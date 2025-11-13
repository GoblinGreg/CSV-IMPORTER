# Używamy oficjalnego obrazu Python 3.11
FROM python:3.11-slim

# Ustawiamy zmienne środowiskowe
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=5000

# Tworzymy katalog roboczy
WORKDIR /app

# Kopiujemy plik z zależnościami
COPY requirements.txt .

# Instalujemy zależności
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy resztę aplikacji
COPY . .

# Otwieramy port 5000
EXPOSE 5000

# Uruchamiamy aplikację przez gunicorn (lepsze niż flask run w produkcji)
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app
