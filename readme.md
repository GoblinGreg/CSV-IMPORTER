# CSV Importer - Flask Application

Aplikacja Flask do importowania plików CSV do bazy danych MySQL. Projekt jest w fazie rozwoju - obecnie zawiera podstawową strukturę z API endpoints, Dockerem i CI/CD.

## 🚀 Funkcjonalności (obecne)

- ✅ Podstawowa aplikacja Flask z trzema endpointami
- ✅ Testy automatyczne używające biblioteki `requests`
- ✅ Dockeryzacja aplikacji
- ✅ CI/CD pipeline przez GitHub Actions i Railway

## 📋 Wymagania

- Python 3.11+
- Docker (opcjonalnie)
- Git

## 🛠️ Instalacja lokalna

### 1. Klonowanie repozytorium

```bash
git clone <url-twojego-repo>
cd <nazwa-folderu>
```

### 2. Utworzenie środowiska wirtualnego

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# lub
venv\Scripts\activate  # Windows
```

### 3. Instalacja zależności

```bash
pip install -r requirements.txt
```

### 4. Uruchomienie aplikacji

```bash
python app.py
```

Aplikacja będzie dostępna pod adresem: `http://localhost:5000`

## 🧪 Testowanie

Aby przetestować aplikację, uruchom:

```bash
# W jednym terminalu uruchom aplikację
python app.py

# W drugim terminalu uruchom testy
python test_app.py
```

## 🐳 Docker

### Budowanie obrazu

```bash
docker build -t csv-importer .
```

### Uruchomienie kontenera

```bash
docker run -p 5000:5000 csv-importer
```

Aplikacja będzie dostępna pod adresem: `http://localhost:5000`

### Wyjaśnienie Dockerfile:

1. **FROM python:3.11-slim** - używamy lekkiego obrazu Python 3.11
2. **ENV** - ustawiamy zmienne środowiskowe (PYTHONUNBUFFERED zapobiega buforowaniu logów)
3. **WORKDIR /app** - tworzymy i ustawiamy katalog roboczy
4. **COPY requirements.txt** - najpierw kopiujemy tylko requirements (cache Docker)
5. **RUN pip install** - instalujemy zależności
6. **COPY . .** - kopiujemy resztę aplikacji
7. **EXPOSE 5000** - dokumentujemy, że używamy portu 5000
8. **CMD gunicorn** - uruchamiamy aplikację przez gunicorn (serwer produkcyjny)

## 🔄 CI/CD - GitHub Actions + Railway

### Konfiguracja Railway:

1. **Załóż konto na Railway.app**
   - Przejdź na https://railway.app/
   - Zaloguj się przez GitHub

2. **Utwórz nowy projekt**
   - Kliknij "New Project"
   - Wybierz "Deploy from GitHub repo"
   - Wybierz swoje repozytorium

3. **Pobierz Railway Token**
   - Przejdź do Account Settings → Tokens
   - Utwórz nowy token: "Create Token"
   - Skopiuj wygenerowany token

4. **Konfiguracja GitHub Secrets**
   - W swoim repozytorium GitHub przejdź do: Settings → Secrets and variables → Actions
   - Dodaj nowy secret:
     - Name: `RAILWAY_TOKEN`
     - Value: <wklej token z Railway>
   - Dodaj drugi secret:
     - Name: `RAILWAY_SERVICE_NAME`
     - Value: <nazwa twojej usługi na Railway (np. "csv-importer")>

### Jak działa workflow:

1. **Trigger** - Workflow uruchamia się automatycznie przy push do branch `main`

2. **Job: test**
   - Checkout kodu z repozytorium
   - Instalacja Python 3.11
   - Instalacja zależności z requirements.txt
   - Uruchomienie aplikacji Flask w tle
   - Uruchomienie testów z `test_app.py`

3. **Job: deploy**
   - Uruchamia się tylko jeśli testy przeszły
   - Uruchamia się tylko dla branch `main`
   - Instaluje Railway CLI
   - Deployuje aplikację na Railway

### Pierwsze wdrożenie:

```bash
# 1. Commituj zmiany
git add .
git commit -m "Initial setup with CI/CD"

# 2. Wypushuj na GitHub
git push origin main

# 3. Sprawdź status w GitHub Actions (zakładka Actions w repo)
```

## 📁 Struktura projektu

```
.
├── app.py                      # Główna aplikacja Flask
├── test_app.py                 # Testy używające requests
├── requirements.txt            # Zależności Python
├── Dockerfile                  # Konfiguracja Docker
├── .dockerignore              # Pliki ignorowane przez Docker
├── .github/
│   └── workflows/
│       └── deploy.yml         # GitHub Actions workflow
└── README.md                  # Ten plik
```

## 🌐 Dostępne endpointy

| Endpoint | Metoda | Opis |
|----------|--------|------|
| `/` | GET | Strona główna z podstawowymi informacjami |
| `/health` | GET | Sprawdzenie statusu aplikacji |
| `/api/info` | GET | Lista dostępnych endpointów |

## 🔮 Planowane funkcjonalności

- [ ] Upload plików CSV
- [ ] Parser CSV
- [ ] Integracja z MySQL przez SQLAlchemy
- [ ] Frontend do uploadowania plików
- [ ] Walidacja danych CSV
- [ ] Historia importów
- [ ] Obsługa błędów importu

## 🐛 Rozwiązywanie problemów

### Aplikacja nie startuje
```bash
# Sprawdź czy port 5000 nie jest zajęty
lsof -i :5000  # Linux/Mac
netstat -ano | findstr :5000  # Windows
```

### Docker build fails
```bash
# Wyczyść cache Dockera
docker system prune -a
```

### Railway deployment fails
- Sprawdź czy token jest poprawny w GitHub Secrets
- Sprawdź logi w Railway dashboard
- Upewnij się że nazwa service jest poprawna

## 📝 Licencja

Ten projekt jest własnością prywatną i służy celom edukacyjnym.

## 👤 Autor

Twoje imię/nazwa
