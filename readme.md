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

## Docker

Build and run the image (it uses the `DATABASE_URL` env var if you provide it):

```bash
docker build -t csv-importer .
docker run -p 5000:5000 -e DATABASE_URL="mysql+pymysql://user:pass@host:3306/db" csv-importer
```

## Files changed/added

- Updated: `app.py` — added SQLAlchemy model, CSV upload, templates usage
- Added: `templates/index.html`, `templates/import_detail.html`, `static/style.css`
- Updated: `requirements.txt` — added `Flask-SQLAlchemy`, `pandas`, `PyMySQL`
- Updated: `dockerfile` — run `main:app` with gunicorn

## How CSVs are stored

Each CSV row is stored as a separate row in the `CsvImport` table with a JSON column `row_data`. This keeps the model flexible for arbitrary CSV schemas.

## Next steps (optional)

- Add a migration workflow (Alembic) for schema evolution
- Add validations and column mapping UI for stronger typing
- Add tests that create a temporary database and assert imports

If you want, mogę teraz uruchomić aplikację lokalnie i przetestować upload (potrzebuję pozwolenia aby uruchomić polecenia tu), albo przygotować zmiany dla deploymentu (GitHub Actions / Railway) — daj znać.
# CSV Importer - Flask Application

A Flask application for importing CSV files into a MySQL database. This project is currently under development and includes basic structure with API endpoints, Docker support, and automated testing.

## Current Features

- Basic Flask application with three endpoints
- Automated tests using the `requests` library
- Docker containerization
- CI/CD pipeline through GitHub Actions

## Requirements

- Python 3.11+
- Docker (optional)
- Git


## Local Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <folder-name>
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## Testing

To test the application:

```bash
# In one terminal, run the application
python app.py

# In another terminal, run tests
python test_app.py
```

## Docker

### Building the image

```bash
docker build -t csv-importer .
```

### Running the container

```bash
docker run -p 5000:5000 csv-importer
```

The application will be available at: `http://localhost:5000`

### Dockerfile explanation:

1. **FROM python:3.11-slim** - uses lightweight Python 3.11 image
2. **ENV** - sets environment variables (PYTHONUNBUFFERED prevents log buffering)
3. **WORKDIR /app** - creates and sets working directory
4. **COPY requirements.txt** - copies requirements first (for Docker cache)
5. **RUN pip install** - installs dependencies
6. **COPY . .** - copies the rest of the application
7. **EXPOSE 5000** - documents that port 5000 is used
8. **CMD gunicorn** - runs the application with gunicorn (production server)

## Project Structure

```
.
├── app.py                      # Main Flask application
├── main.py                     # Gunicorn entry point
├── test_app.py                 # Tests using requests
├── requirements.txt            # Python dependencies
├── Procfile                    # Heroku/Railway deployment config
├── Dockerfile                  # Docker configuration
├── .dockerignore              # Files ignored by Docker
├── .gitignore                 # Files ignored by Git
├── .github/
│   └── workflows/
│       └── deploy.yml         # GitHub Actions workflow
└── README.md                  # This file
```

## Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main page with basic information |
| `/health` | GET | Application health check |
| `/api/info` | GET | List of available endpoints |

## Planned Features

- CSV file upload
- CSV parser
- MySQL integration via SQLAlchemy
- Frontend for file uploads
- CSV data validation
- Import history
- Import error handling

## Troubleshooting

### Application won't start
```bash
# Check if port 5000 is already in use
lsof -i :5000  # Linux/Mac
netstat -ano | findstr :5000  # Windows
```

### Docker build fails
```bash
# Clear Docker cache
docker system prune -a
```

## License

This project is private property and serves educational purposes.

## Author

Grzegorz P (GoblinGreg)