# Demo-G6 Testing Guide

## Komplett Test Suite

Projektet har 90 automatiserade tester som täcker alla delar av applikationen.

## Kör Alla Tester

### Alternativ 1: Test Runner Script (Rekommenderat)
```bash
python run_tests.py
```

### Alternativ 2: Direkt med pytest
```bash
python -m pytest tests/ -v --tb=short
```

### Alternativ 3: Med Coverage Rapport
```bash
python run_tests.py --coverage
```

## Test Översikt

Projektet har 8 test-filer med totalt 90 tester:

| Test Fil | Antal Tester | Beskrivning |
|----------|--------------|-------------|
| `test_smoke.py` | 4 | Grundläggande app-funktionalitet |
| `test_routes.py` | 10 | HTTP routes och templates |
| `test_subscription_service.py` | 19 | Business layer validering |
| `test_subscriber_repository.py` | 14 | Databas-operationer |
| `test_form_submission.py` | 11 | End-to-end formulär-hantering |
| `test_auth_service.py` | 10 | Autentisering och lösenord |
| `test_protected_routes.py` | 10 | Login/logout och skyddade sidor |
| `test_security.py` | 12 | Security headers och error pages |

## Kör Specifika Tester

### Endast en test-fil
```bash
python -m pytest tests/test_smoke.py -v
```

### Endast en test-klass
```bash
python -m pytest tests/test_auth_service.py::TestCreateUser -v
```

### Endast ett specifikt test
```bash
python -m pytest tests/test_smoke.py::test_app_exists -v
```

## Test Fixtures

### `app` fixture
Skapar en test-instans av Flask-appen med in-memory SQLite databas.

### `client` fixture
HTTP test-klient för att simulera requests.

### `authenticated_client` fixture
Förautentiserad klient för att testa skyddade routes.

### `runner` fixture
CLI test runner för att testa Flask-kommandon.

## CI/CD Integration

Testerna körs automatiskt i GitHub Actions vid varje push och pull request.

Se `.github/workflows/` för CI/CD konfiguration.

## Felsökning

### "pytest not found"
Aktivera virtual environment:
```bash
source .venv/bin/activate
```

### "No module named application"
Kör från projekt root:
```bash
cd /Users/ludwigsevenheim/Demo-G6
python run_tests.py
```

### Tester misslyckas lokalt men inte i CI
Kontrollera att du har rätt Python-version (3.10+) och uppdaterade dependencies:
```bash
pip install -r requirements.txt
```

## Test-Driven Development

1. Skriv test först (Red)
2. Implementera minimal kod för att få testet att passa (Green)
3. Refaktorera kod (Refactor)

Kör tester ofta under utveckling:
```bash
# Watch mode (kräver pytest-watch)
ptw tests/
```

## Coverage Report

För att se vilka delar av koden som saknar test-täckning:

```bash
python run_tests.py --coverage
open htmlcov/index.html
```

Målsättning: >80% code coverage

## Best Practices

✅ Kör alla tester innan du pushar kod
✅ Skriv tester för nya features
✅ Håll tester snabba (in-memory databas)
✅ Använd beskrivande test-namn
✅ Ett test testar en sak
✅ Tester ska vara oberoende av varandra
