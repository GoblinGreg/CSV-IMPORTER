from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

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


class CsvImport(db.Model):
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


# Note: table creation moved to `main.py` to avoid using removed Flask 3 decorator


@app.route('/')
def home():
    """Render upload page and recent imports"""
    imports = CsvImport.query.order_by(
        CsvImport.imported_at.desc()).limit(50).all()
    return render_template('index.html', imports=imports)


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('home'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('home'))
    try:
        # Read CSV into pandas (handles headers automatically)
        df = pd.read_csv(file)
        count = 0
        for _, row in df.iterrows():
            rec = CsvImport(filename=file.filename,
                            row_data=row.dropna().to_dict())
            db.session.add(rec)
            count += 1
        db.session.commit()
        flash(f'Imported {count} rows from {file.filename}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error importing CSV: {e}', 'danger')
    return redirect(url_for('home'))


@app.route('/imports/<int:import_id>')
def import_detail(import_id):
    rec = CsvImport.query.get_or_404(import_id)
    return render_template('import_detail.html', rec=rec)


@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'csv-importer'}), 200


@app.route('/api/info')
def api_info():
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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
