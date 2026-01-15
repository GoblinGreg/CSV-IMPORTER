# CSV Importer - Flask Application

Simple Flask app to upload CSV files and store rows in a database.

Key features added:

- Web UI to upload CSV files (HTML + Bootstrap)
- Backend CSV parsing via pandas
- Storage of each row as JSON in a SQL database via SQLAlchemy
- Default uses local SQLite for convenience; supports MySQL via `DATABASE_URL`

## Requirements

- Python >=3.11,<3.12
- Docker (optional)
- Git

## Local Installation

1. Create virtual environment and activate it:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run locally (default: sqlite used if DATABASE_URL not set):

```bash
# Run app (development)
python main.py
```

Open http://localhost:5000 in your browser.

## MySQL (production) setup

To use a MySQL database, set the `DATABASE_URL` environment variable to a SQLAlchemy-compatible URL. Example:

```
mysql+pymysql://DB_USER:DB_PASS@DB_HOST:3306/DB_NAME
```

On Windows PowerShell you can export it like:

```powershell
$env:DATABASE_URL = "mysql+pymysql://user:pass@host:3306/dbname"
python main.py
```

Notes:
- Create the database/schema in MySQL before running the app.
- The app will call `db.create_all()` on first request to create the needed table.

## Using a .env file (recommended)

To avoid exporting `DATABASE_URL` and `SECRET_KEY` each time, create a `.env` file in the project root. See `.env.example` for placeholders. The app uses `python-dotenv` to load variables automatically when the app starts.

Example `.env` values:

```
DATABASE_URL=mysql+pymysql://user:pass@host:3306/dbname
SECRET_KEY=your-secure-secret
```

## Docker

Build and run the image (it uses the `DATABASE_URL` env var if you provide it):

```bash
docker build -t csv-importer .
```

To connect to MySQL on your host machine, use `host.docker.internal` instead of `localhost`:

```bash
docker run -p 5000:5000 -e DATABASE_URL="mysql+pymysql://user:pass@host.docker.internal:3306/dbname" csv-importer
```

Or to use SQLite (default, no external DB needed):

```bash
docker run -p 5000:5000 csv-importer
```

## Files changed/added

- **Refactored:** `app.py` — cleaned up structure: removed duplicates, organized into sections (imports → config → models → helpers → routes → entry point)
- **Updated:** `main.py` — added proper Flask host/port binding for Docker compatibility
- **Updated:** `dockerfile` — removed gunicorn, now uses `python main.py` with JSON CMD format
- **Updated:** `requirements.txt` — removed gunicorn (no longer needed)
- **Removed:** `procfile` — not needed for GitHub Actions deployments
- **Added:** `templates/index.html`, `templates/import_detail.html`, `static/style.css` — web UI for uploads
- **Updated:** `README.md` — complete setup and deployment docs

## How CSVs are stored

Each CSV row is stored as a separate row in the `CsvImport` table with a JSON column `row_data`. This keeps the model flexible for arbitrary CSV schemas.

## Next steps (optional)

- Add a migration workflow (Alembic) for schema evolution
- Add validations and column mapping UI for stronger typing
- Add tests that create a temporary database and assert imports

## License

This project is private property and serves educational purposes.

## Author

Grzegorz P (GoblinGreg)