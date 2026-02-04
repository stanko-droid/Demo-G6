# ARCHITECTURE COMPARISON & VISUAL GUIDE

**Datum:** 4 februari 2026  
**Purpose:** Visuell representation av de två projekten och hur de integreras med Demo-G6

---

## CURRENT STATE vs FUTURE STATE

### CURRENT STATE: Demo-G6 (Stand-alone)
```
┌─────────────────────────────────────────────────────┐
│                    Demo-G6                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │  PRESENTATION LAYER                           │  │
│  │  ├── Routes (Flask blueprints)                │  │
│  │  ├── Templates (HTML/Jinja2)                 │  │
│  │  └── Static assets (CSS/JS)                  │  │
│  └───────────────────────────────────────────────┘  │
│                      ↓                              │
│  ┌───────────────────────────────────────────────┐  │
│  │  BUSINESS LAYER                               │  │
│  │  ├── Services                                 │  │
│  │  ├── Business Logic                          │  │
│  │  └── Data Validation                         │  │
│  └───────────────────────────────────────────────┘  │
│                      ↓                              │
│  ┌───────────────────────────────────────────────┐  │
│  │  DATA LAYER                                   │  │
│  │  ├── Models (SQLAlchemy ORM)                 │  │
│  │  ├── Repositories                            │  │
│  │  └── Database (SQLite/PostgreSQL)            │  │
│  └───────────────────────────────────────────────┘  │
│                                                     │
│  ❌ NO CI/CD PIPELINE                              │
│  ❌ NO AZURE INTEGRATION                           │
│  ✅ LOCAL DOCKER READY                             │
│                                                     │
└─────────────────────────────────────────────────────┘

         ↓ Manual Deployment
         
    Docker Container (Local)
         or
    Simple Server (Manual)
```

### FUTURE STATE: Demo-G6 + CICD (After Integration)
```
┌────────────────────────────────────────────────────────────────────┐
│                        GITHUB REPOSITORY                           │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  CODE & CONFIGURATION                                       │  │
│  │  ├── app/ (3-tier structure)                               │  │
│  │  ├── migrations/ (Alembic)                                 │  │
│  │  ├── .github/workflows/deploy.yml  ← NEW FROM HELLO-CICD  │  │
│  │  ├── Dockerfile                 ← UPDATED                 │  │
│  │  ├── entrypoint.sh              ← NEW                      │  │
│  │  ├── .dockerignore              ← NEW FROM HELLO-CICD      │  │
│  │  └── .azure-config              ← NEW FROM HELLO-CICD      │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                    │
│                                    ↓ git push main                │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  GITHUB ACTIONS (AUTOMATED)                                │  │
│  │  ┌─────────────────────────────────────────────────────┐   │  │
│  │  │ Step 1: Azure Login (OIDC)                          │   │  │
│  │  │ Step 2: Build Docker Image                         │   │  │
│  │  │ Step 3: Push to ACR                                │   │  │
│  │  │ Step 4: Update Container App                       │   │  │
│  │  │ Step 5: Health Check (5 retries)                   │   │  │
│  │  └─────────────────────────────────────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

                            ↓

┌────────────────────────────────────────────────────────────────────┐
│                        AZURE CLOUD                                 │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌──────────────────────┐      ┌──────────────────────────────┐  │
│  │  AZURE CONTAINER     │      │  AZURE CONTAINER APP         │  │
│  │  REGISTRY (ACR)      │      │  (ca-demo-g6)               │  │
│  │                      │  →   │                              │  │
│  │  demo-g6:<sha>       │      │  ┌──────────────────────┐   │  │
│  │  demo-g6:latest      │      │  │  Demo-G6 App        │   │  │
│  └──────────────────────┘      │  │  - Port 5000        │   │  │
│                                │  │  - Auto-scaling     │   │  │
│                                │  │  - Managed SSL      │   │  │
│                                │  │  - Health checks    │   │  │
│                                │  │                     │   │  │
│                                │  │  ┌───────────────┐  │   │  │
│                                │  │  │ Entrypoint:   │  │   │  │
│                                │  │  │ 1. Migrations │  │   │  │
│                                │  │  │ 2. Gunicorn   │  │   │  │
│                                │  │  └───────────────┘  │   │  │
│                                │  └──────────────────────┘   │  │
│                                └──────────────────────────────┘  │
│                                          ↓                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  DATABASE (PostgreSQL/Azure SQL)                           │ │
│  │  ├── Subscribers table                                     │ │
│  │  ├── Other business tables                                │ │
│  │  └── Auto-backups                                         │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  FQDN: ca-demo-g6.<region>.azurecontainerapps.io                │
│  Status: ALWAYS AVAILABLE (managed by Azure)                     │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

         ↓ HTTPS
         
    https://ca-demo-g6.<region>.azurecontainerapps.io
    
    ✅ CI/CD PIPELINE
    ✅ AZURE INTEGRATION
    ✅ AUTOMATIC DEPLOYMENT
    ✅ AUTO-SCALING
    ✅ MANAGED SSL
```

---

## COMPARISON TABLE - 3 TIER ARCHITECTURE

### Hello-CICD Architecture
```
┌─────────────────┐
│   Flask App     │
│   (app.py)      │
│                 │
│  @app.route()   │
│  ↓              │
│  Return HTML    │
└─────────────────┘

❌ No separation of concerns
❌ No database layer
❌ No business logic separation
✅ Simple, minimal
✅ Easy to containerize
```

### Test.3tier Architecture (Proper 3-Tier)
```
PRESENTATION LAYER
┌────────────────────────────────┐
│ Routes (app/presentation/)     │
│ ├── public.py (Blueprint)      │
│ └── templates/                 │
│     ├── index.html             │
│     ├── subscribe.html         │
│     └── thank_you.html         │
└────────────────────────────────┘
            ↓
BUSINESS LAYER
┌────────────────────────────────┐
│ Services (app/business/)       │
│ ├── subscription_service.py    │
│ └── Other business logic       │
└────────────────────────────────┘
            ↓
DATA LAYER
┌────────────────────────────────┐
│ Repositories (app/data/)       │
│ ├── Models (SQLAlchemy)        │
│ │   └── subscriber.py          │
│ └── Repositories               │
│     └── subscriber_repo.py     │
└────────────────────────────────┘
            ↓
DATABASE
┌────────────────────────────────┐
│ SQLite / PostgreSQL / Azure SQL│
│ ├── subscribers table          │
│ └── Other tables               │
└────────────────────────────────┘

✅ Clear separation of concerns
✅ Testable components
✅ Reusable business logic
✅ Scalable architecture
✅ Professional structure
```

### Demo-G6 Architecture (Current)
```
Samma som Test.3tier (redan 3-tier)
+ Kan lägga till Hello-CICD's CI/CD pipeline
= Fullständig DevOps-integrerad app
```

---

## DEPLOYMENT COMPARISON

### Scenario 1: Manual Deployment (Current)
```
Developer
  ↓
git push
  ↓
SSH into server
  ↓
git pull
  ↓
pip install requirements
  ↓
flask db upgrade (manual)
  ↓
restart gunicorn (manual)
  ↓
❌ Time consuming
❌ Error-prone
❌ Difficult to debug
❌ No rollback mechanism
```

### Scenario 2: Automated Azure Deployment (After Integration)
```
Developer
  ↓
git push main
  ↓
GitHub Actions triggers
  ↓
1. Azure Login (OIDC)
  ↓
2. Build Docker image
  ↓
3. Push to ACR
  ↓
4. Deploy to Container App
  ↓
5. Health check
  ↓
6. Automatic scaling
  ↓
✅ Fully automated
✅ Error handling
✅ Rollback capability
✅ Monitoring & alerts
✅ Production-ready
```

---

## FILE STRUCTURE - BEFORE AND AFTER

### BEFORE (Demo-G6 Current)
```
Demo-G6/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── business/
│   │   └── services/
│   │       ├── __init__.py
│   │       └── subscription_service.py
│   ├── data/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── subscriber.py
│   │   └── repositories/
│   │       ├── __init__.py
│   │       ├── joke_repository.py
│   │       └── subscriber_repository.py
│   └── presentation/
│       ├── routes/
│       │   ├── __init__.py
│       │   └── public.py
│       ├── static/
│       │   ├── base.css
│       │   ├── hero.css
│       │   ├── modal.css
│       │   └── style.css
│       └── templates/
│           ├── base.html
│           ├── index.html
│           ├── subscribe.html
│           └── thank_you.html
├── migrations/
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│       └── ce6c6f1249f6_add_subscribers_table.py
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```

### AFTER (Demo-G6 with CI/CD)
```
Demo-G6/
├── .github/                          ← NEW
│   └── workflows/
│       └── deploy.yml                ← NEW (from Hello-CICD)
├── .azure-config                     ← NEW (from Hello-CICD)
├── .dockerignore                     ← NEW (from Hello-CICD)
├── Dockerfile                        ← UPDATED (from Test.3tier)
├── entrypoint.sh                     ← NEW (from Test.3tier)
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── business/
│   │   └── services/
│   │       ├── __init__.py
│   │       └── subscription_service.py
│   ├── data/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── subscriber.py
│   │   └── repositories/
│   │       ├── __init__.py
│   │       ├── joke_repository.py
│   │       └── subscriber_repository.py
│   └── presentation/
│       ├── routes/
│       │   ├── __init__.py
│       │   └── public.py
│       ├── static/
│       │   ├── base.css
│       │   ├── hero.css
│       │   ├── modal.css
│       │   └── style.css
│       └── templates/
│           ├── base.html
│           ├── index.html
│           ├── subscribe.html
│           └── thank_you.html
├── migrations/
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│       └── ce6c6f1249f6_add_subscribers_table.py
├── .gitignore
├── app.py (eller wsgi.py)
├── requirements.txt                  ← UPDATED
├── README.md
├── INTEGRATION_REPORT.md             ← NEW (denna rapport)
└── INTEGRATION_GUIDE.md              ← NEW (praktiska instruktioner)
```

---

## DEPENDENCY GRAPH

### Hello-CICD Dependencies
```
Flask ──┐
        ├─→ Demo-G6
Gunicorn┘
```

### Test.3tier Dependencies
```
Flask ─────────┐
               │
Flask-SQLAlchemy──┐
                  ├─→ Demo-G6
Flask-Migrate────┤
                  │
Python-dotenv────┤
Gunicorn────────┐│
Pyodbc─────────┐││
               └┴┘
```

### Final Demo-G6 + CI/CD Dependencies
```
┌─── Flask & Databases ──────────────────┐
│                                       │
│  Flask                                │
│  Flask-SQLAlchemy                     │
│  Flask-Migrate                        │
│  Python-dotenv                        │
│  Gunicorn                             │
│  Pyodbc (optional for Azure SQL)      │
│                                       │
│  = Full 3-tier + CI/CD support        │
│                                       │
└───────────────────────────────────────┘

+ GitHub Actions
+ Azure Container Registry
+ Azure Container Apps
= Production-ready DevOps setup
```

---

## WORKFLOW COMPARISON

### Hello-CICD Workflow
```
┌─ BUILD STAGE ─┐
│               │
│ Docker Build  │
│ ↓             │
│ ACR Push      │
│               │
└───────────────┘
        ↓
┌─ DEPLOY STAGE ─┐
│                │
│ Container App  │
│ Update         │
│                │
└────────────────┘
        ↓
┌─ VERIFY STAGE ┐
│               │
│ Health Check  │
│ (5 retries)   │
│               │
└───────────────┘
```

### Integrated Workflow (After Integration)
```
┌──── BUILD STAGE ────┐
│                     │
│  Docker Build       │
│  (with migrations)  │
│  ↓                  │
│  ACR Push           │
│                     │
└─────────────────────┘
           ↓
┌──── DEPLOY STAGE ───┐
│                     │
│  Container App      │
│  Update             │
│  Auto-scaling       │
│  Managed SSL        │
│                     │
└─────────────────────┘
           ↓
┌──── VERIFY STAGE ───┐
│                     │
│  Health Check       │
│  Database Check     │
│  (5 retries)        │
│  Alerts on failure  │
│                     │
└─────────────────────┘
           ↓
┌──── MONITOR ────────┐
│                     │
│  Azure Logging      │
│  Performance        │
│  Metrics            │
│  Auto-restart       │
│                     │
└─────────────────────┘
```

---

## TECHNOLOGY STACK

### Before Integration
```
┌─────────────────────────────────┐
│  Technology Stack - Demo-G6     │
├─────────────────────────────────┤
│ Language      │ Python 3.11     │
│ Framework     │ Flask 3.x       │
│ ORM           │ SQLAlchemy      │
│ Database      │ PostgreSQL/SQLite
│ Migration     │ Alembic         │
│ Server        │ Gunicorn        │
│ Container     │ Docker          │
│ Deployment    │ Manual          │
└─────────────────────────────────┘
```

### After Integration (Full Stack)
```
┌──────────────────────────────────────────┐
│  Technology Stack - Demo-G6 + CI/CD      │
├──────────────────────────────────────────┤
│ Language         │ Python 3.11           │
│ Framework        │ Flask 3.x             │
│ ORM              │ SQLAlchemy            │
│ Database         │ PostgreSQL/SQLite/    │
│                  │ Azure SQL             │
│ Migration        │ Alembic               │
│ Server           │ Gunicorn              │
│ Container        │ Docker                │
│ CI/CD            │ GitHub Actions ← NEW  │
│ Registry         │ Azure ACR ← NEW       │
│ Deployment       │ Azure Container ← NEW │
│                  │ Apps                  │
│ IaC              │ (via workflow) ← NEW   │
│ Monitoring       │ Azure Monitor ← NEW   │
└──────────────────────────────────────────┘
```

---

## COST IMPLICATIONS

### Azure Resources (Estimated Monthly)

| Resource | SKU | Monthly Cost |
|----------|-----|--------------|
| Container Registry | Basic | ~10 USD |
| Container Apps | Pay-per-use | ~5-50 USD (scalable) |
| Database (if Azure SQL) | Standard | ~30-100 USD |
| Storage (logs) | Standard | ~1 USD |
| **Total** | | **~50-160 USD** |

**Notes:**
- Container Apps includes 180,000 vCPU-seconds free monthly
- Scales from $0 during zero traffic
- No charges for GitHub Actions (free for public repos)

---

## SUCCESS CRITERIA

After integration, verify:

- [ ] ✅ GitHub Actions workflow triggers on push
- [ ] ✅ Docker image builds successfully
- [ ] ✅ Image pushes to ACR
- [ ] ✅ Container App updates automatically
- [ ] ✅ Database migrations run at startup
- [ ] ✅ Health check passes
- [ ] ✅ App accessible via FQDN (HTTPS)
- [ ] ✅ All existing features work
- [ ] ✅ Databases synced
- [ ] ✅ Rollback procedure tested

---

## FINAL CHECKLIST

Before going live:

- [ ] GitHub Secrets configured (AZURE_CLIENT_ID, etc)
- [ ] Azure resources created (RG, ACR, Container App)
- [ ] OIDC Federation setup complete
- [ ] Dockerfile tested locally
- [ ] Entrypoint script tested
- [ ] Database migrations verified
- [ ] .gitignore updated (.azure-config added)
- [ ] Documentation updated (README)
- [ ] Team trained on deployment process
- [ ] Monitoring alerts configured
- [ ] Rollback plan documented

---

**Document Version:** 1.0  
**Last Updated:** 2026-02-04  
**Status:** Ready for Implementation
