# CSV Importer - Flask Application

A Flask application for importing CSV files into a MySQL database. This project is currently under development and includes basic structure with API endpoints, Docker support, and automated testing.

## Current Features

- Basic Flask application with three endpoints
- Automated tests using the `requests` library
- Docker containerization
- CI/CD pipeline through GitHub Actions and Railway

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
├── test_app.py                 # Tests using requests
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── .dockerignore              # Files ignored by Docker
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