# Guide: Införa 3-Tier Arkitektur i Demo G6

## Översikt
Denna guide visar hur du refaktorerar din Flask-applikation till en **3-tier arkitektur** med följande lager:

- **Data Layer** (`data/`) - Hanterar dataåtkomst och lagring
- **Business Layer** (`business/`) - Innehåller affärslogik och regler
- **Presentation Layer** (`presentation/`) - Flask routes och användargränssnitt

## Nuvarande Struktur (Monolitisk)
```
Demo-G6/
├── app.py              # Allt i en fil (routes, data, logik)
├── templates/
├── static/
└── requirements.txt
```

## Ny Struktur (3-Tier)
```
Demo-G6/
├── app.py              # Huvudapplikation (entry point)
├── data/               # Data Layer
│   ├── __init__.py
│   └── joke_repository.py
├── business/           # Business Layer
│   ├── __init__.py
│   └── joke_service.py
├── presentation/       # Presentation Layer
│   ├── __init__.py
│   ├── routes.py
│   └── controllers/
├── templates/
├── static/
└── requirements.txt
```

## Steg-för-Steg Implementation

### Steg 1: Skapa Mappstruktur
```bash
mkdir -p data business presentation/controllers
```

### Steg 2: Data Layer - `data/joke_repository.py`
Skapa repository för datahantering:

```python
# data/joke_repository.py
class JokeRepository:
    def __init__(self):
        self.jokes = [
            "Varför var matematikboken ledsen? Den hade för många problem.",
            "Vad sa den ena väggen till den andra? Vi ses vid hörnet!",
            "Vilket djur är bäst på att smyga? Mysk-oxen.",
            "Hur vet man att en bil är från Tyskland? Det hörs på lacken!",
            "Det var en gång två bagare och en smet.",
            "Vilken ört läker sår bäst? Timjan.",
            "Vad kallas en överviktig hund? En rundgång.",
            "Varför har inte orienterare några barn? De springer bara runt i buskarna.",
            "Vad sa göteborgaren till den döda fisken? Det var ett jävla liv på dig.",
            "Hur ser man att en dykare är gift? Man ser det på ringarna på vattnet.",
            "Vilken hund är bäst på att trolla? Labra-dabra-dor.",
            "Vad gör en arbetslös skådespelare? Spelar ingen roll.",
            "Vilket land har de sämsta bilarna? Bak-u.",
            "Varför är det svårt att spela kort i djungeln? Det finns för många leoparder.",
            "Vad heter tysklands sämsta bärplockare? Han som hittar-inte.",
            "Vad kallas en kvinna som vet var hennes man är hela tiden? En änka.",
            "Vem är bäst på att tvätta i djungeln? Gor-illa.",
            "Vad sa kaffekoppen till den andra kaffekoppen? Är det bön-söndag idag?",
            "Vilket djur ser sämst? Allt-i-gatorn.",
            "Vad heter världens fattigaste kung? Kung-kurs."
        ]

    def get_all_jokes(self):
        """Returnerar alla skämt"""
        return self.jokes

    def get_joke_by_index(self, index):
        """Returnerar ett specifikt skämt baserat på index"""
        if 0 <= index < len(self.jokes):
            return self.jokes[index]
        return None
```

### Steg 3: Business Layer - `business/joke_service.py`
Skapa service för affärslogik:

```python
# business/joke_service.py
import random
from data.joke_repository import JokeRepository

class JokeService:
    def __init__(self):
        self.joke_repository = JokeRepository()

    def get_random_joke(self):
        """Returnerar ett slumpmässigt skämt"""
        jokes = self.joke_repository.get_all_jokes()
        return random.choice(jokes) if jokes else "Inga skämt tillgängliga"

    def get_all_jokes(self):
        """Returnerar alla skämt"""
        return self.joke_repository.get_all_jokes()

    def get_joke_count(self):
        """Returnerar antal skämt"""
        return len(self.joke_repository.get_all_jokes())
```

### Steg 4: Presentation Layer - `presentation/routes.py`
Flytta routes till separat fil:

```python
# presentation/routes.py
from flask import Blueprint, render_template
from business.joke_service import JokeService

# Skapa Blueprint för presentation layer
presentation_bp = Blueprint('presentation', __name__)

# Initiera service
joke_service = JokeService()

@presentation_bp.route('/')
def home():
    """Huvudsidan med slumpmässigt skämt"""
    joke = joke_service.get_random_joke()
    joke_count = joke_service.get_joke_count()

    return render_template('index.html',
                         version='G6-SLAY-ULTIMATE',
                         joke=joke,
                         joke_count=joke_count)

@presentation_bp.route('/api/jokes')
def get_all_jokes():
    """API endpoint för alla skämt"""
    jokes = joke_service.get_all_jokes()
    return {'jokes': jokes, 'count': len(jokes)}
```

### Steg 5: Uppdatera `app.py`
Refaktorisera huvudfilen:

```python
# app.py
from flask import Flask
from presentation.routes import presentation_bp

def create_app():
    """Application Factory Pattern"""
    app = Flask(__name__)

    # Registrera blueprints
    app.register_blueprint(presentation_bp)

    return app

# För development
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
```

### Steg 6: Skapa `__init__.py` filer
```python
# data/__init__.py
from .joke_repository import JokeRepository

__all__ = ['JokeRepository']

# business/__init__.py
from .joke_service import JokeService

__all__ = ['JokeService']

# presentation/__init__.py
from .routes import presentation_bp

__all__ = ['presentation_bp']
```

## Fördelar med 3-Tier Arkitektur

### 🏗️ **Separation of Concerns**
- **Data Layer**: Endast datahantering
- **Business Layer**: Endast affärslogik
- **Presentation Layer**: Endast användargränssnitt

### 🔧 **Underhållbarhet**
- Lätt att ändra ett lager utan att påverka andra
- Tydliga gränser mellan olika ansvarsområden

### 🧪 **Testbarhet**
- Varje lager kan testas separat
- Mock dependencies för enhetstester

### 📈 **Skalbarhet**
- Lätt att lägga till nya funktioner
- Kan enkelt byta ut hela lager (t.ex. databas)

### 🔄 **Återanvändbarhet**
- Business logic kan återanvändas i andra presentation layers
- Data access kan användas av flera services

## Implementation i Demo G6

Följ stegen ovan för att skapa följande struktur:

```
Demo-G6/
├── app.py                    # Entry point
├── data/
│   ├── __init__.py
│   └── joke_repository.py    # Data access
├── business/
│   ├── __init__.py
│   └── joke_service.py       # Business logic
├── presentation/
│   ├── __init__.py
│   ├── routes.py            # Flask routes
│   └── controllers/         # Framtida controllers
├── templates/
├── static/
└── requirements.txt
```

## Nästa Steg

1. **Databas Integration**: Ersätt hårdkodade skämt med databas
2. **API Layer**: Lägg till REST API endpoints
3. **Authentication**: Lägg till användarhantering
4. **Testing**: Skriv enhetstester för varje lager
5. **Configuration**: Lägg till konfigurationshantering

## Kör Applikationen

Efter implementation:

```bash
cd Demo-G6
python app.py
```

Besök `http://localhost:5000` för att se resultatet.

---

*Denna guide skapar en solid grund för vidareutveckling av Demo G6 med professionell arkitektur.*