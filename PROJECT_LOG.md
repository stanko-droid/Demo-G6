# Demo-G6 Project Log - 28 Januari 2026

## Överblick
Implementering av övningar 4-8 från DevOps PM-kursen med fokus på 3-tier arkitektur, databaskonfiguration och UI-design.

---

## Dag: 28 Januari 2026

### Session 1: Layout och Design Förbättringar

#### Ändringar Gjorda:

1. **Hero Section Flytt**
   - Flyttade "Stay Ahead of the Curve"-sektionen från toppen till botten av sidan
   - Sektion ligger nu tillsammans med Subscribe-knappen
   - Detta skapade bättre visuell flöde på hemsidan

2. **DevOps Text Positionering**
   - Flyttade "PREMIER LEAGUE DEVOPS: 2" text längst ner på sidan
   - Placerades efter Subscribe-knappen i footern
   - Säkerställer att footer-informationen ligger nederst

3. **Version Uppdatering**
   - Ändrade version från 1 till 2
   - Uppdaterad i footer-sektionen

4. **Neon Blink Effect**
   - Lade till rosa neon-blink animation på "STREET WISDOM:" texten
   - CSS animation: `neon-flicker` med 0.15s intervall
   - Färg: `#ff006e` (hot pink) med text-shadow glow-effekt
   - Flickrar mellan två rosa nyanser för neon-ljus effekt

#### Sidlayout (Final):
```
1. G6 Header + SLAY Tag
2. Music Player & Joke Generator Buttons
3. STREET WISDOM Joke Card (med neon-blink)
4. Stay Ahead of the Curve Hero Section
5. Subscribe Now Button
6. DevOps Version Footer (längst ner)
7. Cloud Animations (fixed background)
```

---

## Implementerade Features (Tidigare Sessioner)

### Exercise 4: Hero Section & Modal
- ✅ Hero sektion med 135° blå gradient
- ✅ Responsiv modal dialog med ARIA-attribut för accessibility
- ✅ Separerad CSS: base.css, hero.css, modal.css

### Exercise 5: Subscription Form
- ✅ GET /subscribe route med subscription form
- ✅ POST /subscribe/confirm route för form-hantering
- ✅ thank_you.html bekräftelsesida
- ✅ Form validering och error-hantering
- ✅ Input-värden sparas vid fel

### Exercise 6: Database Setup
- ✅ Flask-SQLAlchemy integration
- ✅ Flask-Migrate för database migrations
- ✅ SQLite database (instance/news_flash.db)
- ✅ Subscriber model med: id, email, name, subscribed_at

### Exercise 7: Repository Pattern & Full Integration
- ✅ SubscriberRepository med CRUD-operationer
- ✅ SubscriptionService med validering och normalisering
- ✅ 3-tier arkitektur: Presentation → Business → Data
- ✅ Email validering (regex)
- ✅ Email normalisering (lowercase, trim)
- ✅ Duplicate detection
- ✅ Alla tester passerade (7/7)

### Exercise 8: Design Changes
- ✅ Subscribe Now knapp flytt från hero till bottom
- ✅ Hero sektion flytt ned
- ✅ DevOps text längst ner
- ✅ Version uppdatering till 2
- ✅ Neon blink effekt på "STREET WISDOM"

---

## Git Commits Idag

| Commit | Branch | Meddelande |
|--------|--------|-----------|
| 2cc2b01 | G6-30-Userstory-8-design-changes | G6-31 Userstory 8 - Move hero section and DevOps text, update version to 2 |
| d0c4209 | G6-30-Userstory-8-design-changes | G6-30 Userstory 8 - Move hero section and DevOps text, update version to 2 (amended) |
| d0c4209 | main | Merge G6-30 design changes into main |
| Latest | main | (Pushed to origin/main) |

**Merge Conflict Resolution:**
- Löste merge conflict i app/presentation/templates/index.html
- Accepterade remote version (G6-30 branch) som source of truth
- Merged in main med commit "Merge G6-30 design changes into main"

---

## Teknisk Stack

### Backend
- **Framework:** Flask 3.14 (Python 3.14)
- **ORM:** SQLAlchemy 2.0+ med Flask-SQLAlchemy
- **Migrations:** Flask-Migrate 4.0+ (Alembic)
- **Database:** SQLite (instance/news_flash.db)

### Arkitektur
- **3-Tier Architecture:** 
  - Data Layer: SubscriberRepository
  - Business Layer: SubscriptionService
  - Presentation Layer: Flask routes + Jinja2 templates

### Frontend
- **Templating:** Jinja2 med template inheritance
- **CSS:** BEM naming convention
- **Animations:** Keyframe animations (clouds, neon-blink)
- **Accessibility:** ARIA attributes, semantic HTML

---

## Databas Schema

**Subscribers Table:**
```sql
CREATE TABLE subscribers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL DEFAULT 'Subscriber',
    subscribed_at DATETIME NOT NULL DEFAULT (datetime('now', 'utc'))
);
```

**Test Data:**
- john@example.com (John Doe)
- jane@example.com (Jane Smith)
- bob@example.com (Subscriber)
- fadhil.luqman@gmail.live (Fadhil)

---

## CSS Animations Tillagda

### Neon Blink Effect
```css
.neon-blink {
    color: #ff006e;
    text-shadow: 0 0 10px #ff006e, 0 0 20px #ff006e, 0 0 30px #ff006e;
    animation: neon-flicker 0.15s infinite;
}

@keyframes neon-flicker {
    0%, 100% { 
        color: #ff006e;
        text-shadow: 0 0 10px #ff006e, 0 0 20px #ff006e, 0 0 30px #ff006e;
    }
    50% {
        color: #ff1493;
        text-shadow: 0 0 5px #ff006e, 0 0 10px #ff006e;
    }
}
```

---

## Status: ✅ COMPLETE

Alla övningar implementerade, testade och deployade till main branch.
Applikationen är redo för produktion eller vidare utveckling.

**Uppdaterad:** 28 Jan 2026
**Branch:** main
**Version:** 2.0
