"""
CSV Importer Flask Application

A Flask app for uploading CSV files, parsing them, and importing data into MySQL via SQLAlchemy.
Dynamically creates timestamped tables for each CSV import and maintains an audit log.
"""

from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import re
from sqlalchemy import MetaData, Table, Column
from sqlalchemy import Integer, Float, String, DateTime, Text


# =============================================================================
# INITIALIZATION & CONFIGURATION
# =============================================================================

# Load environment variables from .env if present
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'devkey')

# Database configuration: use DATABASE_URL env var (e.g. mysql+pymysql://user:pass@host:3306/db)
# Fallback to sqlite for local development
database_url = os.environ.get('DATABASE_URL') or 'sqlite:///data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# =============================================================================
# MODELS
# =============================================================================

class CsvImport(db.Model):
    """Audit log model: tracks each CSV upload and stores sample row data as JSON."""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256))
    imported_at = db.Column(db.DateTime, default=datetime.utcnow)
    row_data = db.Column(db.JSON)

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'imported_at': self.imported_at.isoformat(),
            'row_data': self.row_data,
        }


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _sanitize_table_name(name: str) -> str:
    """Sanitize filename to valid SQL table name (lowercase, alphanumeric + underscore)."""
    base = os.path.splitext(name)[0]
    cleaned = re.sub(r'[^0-9a-zA-Z]+', '_', base)
    cleaned = cleaned.strip('_').lower()
    return cleaned


def create_dynamic_table_from_csv(file, filename: str) -> str:
    """
    Create and populate a dynamic table for a given CSV file.

    - Reads the CSV file into a pandas DataFrame
    - Maps pandas dtypes to SQL types (int→Integer, float→Float, object→String(255), datetime→DateTime, else→Text)
    - Creates table with sanitized filename + timestamp (format: data_{filename}_{YYYYMMDD_HHMMSS})
    - Inserts DataFrame rows into the new table
    - Returns the created table name

    Args:
        file: FileStorage object (from request.files)
        filename: Original filename for table naming

    Returns:
        str: Name of the created table

    Raises:
        ValueError: If CSV cannot be read or is empty
    """
    try:
        file.seek(0)
    except Exception:
        pass

    try:
        df = pd.read_csv(file)
    except Exception as e:
        raise ValueError(f'Unable to read CSV: {e}')

    if df.empty:
        raise ValueError('CSV is empty')

    # Generate timestamped table name
    ts = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    safe_base = _sanitize_table_name(filename)
    table_name = f'data_{safe_base}_{ts}'

    # Build column definitions with type mapping
    metadata = MetaData()
    cols = []
    cols.append(Column('id', Integer, primary_key=True, autoincrement=True))

    col_rename_map = {}
    for col in df.columns:
        dtype = str(df[col].dtype)
        sanitized_col = re.sub(r'[^0-9a-zA-Z]+', '_', str(col)).strip('_')
        if sanitized_col == '':
            sanitized_col = 'col'
        # Ensure unique column names
        orig = sanitized_col
        i = 1
        while sanitized_col in col_rename_map.values():
            sanitized_col = f"{orig}_{i}"
            i += 1
        col_rename_map[col] = sanitized_col

        # Map pandas dtype to SQLAlchemy type
        if 'int' in dtype:
            col_type = Integer
        elif 'float' in dtype:
            col_type = Float
        elif 'datetime' in dtype:
            col_type = DateTime
        elif dtype == 'object':
            col_type = String(255)
        else:
            col_type = Text

        cols.append(Column(sanitized_col, col_type))

    # Add audit columns
    cols.append(Column('imported_at', DateTime))
    cols.append(Column('source_filename', String(255)))

    # Create table and insert data
    table = Table(table_name, metadata, *cols)
    metadata.create_all(bind=db.engine)

    df_insert = df.rename(columns=col_rename_map)
    df_insert['imported_at'] = datetime.utcnow()
    df_insert['source_filename'] = filename

    try:
        df_insert.to_sql(table_name, con=db.engine,
                         if_exists='append', index=False)
    except Exception:
        try:
            table.drop(bind=db.engine)
        except Exception:
            pass
        raise

    return table_name


# =============================================================================
# ROUTES
# =============================================================================

@app.route('/')
def home():
    """Render upload page and display recent imports."""
    imports = CsvImport.query.order_by(
        CsvImport.imported_at.desc()).limit(50).all()
    return render_template('index.html', imports=imports)


@app.route('/upload', methods=['POST'])
def upload():
    """
    Handle CSV file upload.

    Flow:
    1. Validate file is present and is a CSV
    2. Parse CSV and save audit log entries
    3. Create dynamic table and insert data
    4. Return JSON (for API/AJAX) or redirect to home with flash (for browser forms)

    Returns:
        - HTML redirect + flash message if this is a standard browser form submit
        - JSON response if this is an API/AJAX request
    """
    # Debug: log incoming headers to diagnose request type
    try:
        print('[UPLOAD] Content-Type:', request.content_type)
        print('[UPLOAD] Accept:', request.headers.get('Accept'))
        print('[UPLOAD] X-Requested-With:',
              request.headers.get('X-Requested-With'))
    except Exception:
        pass

    # Validate file presence
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Validate file is CSV
    if not file.filename.lower().endswith('.csv'):
        return jsonify({'error': 'Uploaded file is not a CSV'}), 400

    # Parse CSV
    try:
        try:
            file.seek(0)
        except Exception:
            pass
        df = pd.read_csv(file)
    except Exception as e:
        return jsonify({'error': f'Unable to read CSV: {e}'}), 400

    if df.empty:
        return jsonify({'error': 'CSV is empty'}), 400

    # Save audit log entries (one per CSV row)
    try:
        count = 0
        for _, row in df.iterrows():
            rec = CsvImport(filename=file.filename,
                            row_data=row.dropna().to_dict())
            db.session.add(rec)
            count += 1
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error saving audit log: {e}'}), 500

    # Create dynamic table and insert data
    try:
        try:
            file.seek(0)
        except Exception:
            pass
        table_name = create_dynamic_table_from_csv(file, file.filename)
    except Exception as e:
        return jsonify({'error': f'Error creating dynamic table: {e}'}), 500

    response_data = {'message': 'Import successful',
                     'table_name': table_name, 'rows_imported': count}

    # Decide response format: HTML redirect for browser forms, JSON for API
    content_type = request.content_type or ''
    if content_type.startswith('multipart/form-data'):
        # Standard browser form submit: redirect to home with flash message
        flash(f"Imported {count} rows into {table_name}", 'success')
        return redirect(url_for('home'))

    # Otherwise treat as API/AJAX: return JSON if Accept prefers it or X-Requested-With indicates AJAX
    json_q = request.accept_mimetypes.get('application/json', 0)
    html_q = request.accept_mimetypes.get('text/html', 0)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or json_q > html_q:
        return jsonify(response_data), 200

    # Fallback to HTML redirect
    flash(f"Imported {count} rows into {table_name}", 'success')
    return redirect(url_for('home'))


@app.route('/imports/<int:import_id>')
def import_detail(import_id):
    """Display details of a specific import (audit log entry)."""
    rec = CsvImport.query.get_or_404(import_id)
    return render_template('import_detail.html', rec=rec)


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'csv-importer'}), 200


@app.route('/api/info')
def api_info():
    """API information endpoint: lists available endpoints."""
    return jsonify({
        'endpoints': [
            {'path': '/', 'method': 'GET',
                'description': 'Main Site (upload form)'},
            {'path': '/upload', 'method': 'POST', 'description': 'Upload CSV'},
            {'path': '/health', 'method': 'GET',
                'description': 'Application Status'},
            {'path': '/api/info', 'method': 'GET',
                'description': 'Info About API'},
        ]
    })


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
