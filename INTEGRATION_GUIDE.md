# INTEGRATION GUIDE - PRAKTISKA INSTRUKTIONER

**Datum:** 4 februari 2026  
**Syfte:** Steg-för-steg guide för att integrera CI/CD från Hello-CICD och 3-tier struktur från Test.3tier till Demo-G6

---

## QUICK START INTEGRATION

### 1. KOPIERA CI/CD PIPELINE

#### Steg 1a: Skapa GitHub Actions struktur
```bash
cd /Users/ludwigsevenheim/Demo-G6
mkdir -p .github/workflows
```

#### Steg 1b: Skapa deploy.yml (anpassad för Demo-G6)
```yaml
name: Build and Deploy to Azure

on:
  push:
    branches: [main, G6-31-synkronisera-CICD-och-3tier-databas-till-DEMO-G6]

permissions:
  id-token: write
  contents: read

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: azure/login@v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}

      - name: Build and push to ACR
        run: |
          az acr build \
            --registry ${{ vars.ACR_NAME }} \
            --image demo-g6:${{ github.sha }} .

      - name: Deploy to Container Apps
        run: |
          ACR_SERVER=$(az acr show --name ${{ vars.ACR_NAME }} \
            --query loginServer -o tsv)
          az containerapp update \
            --name ${{ vars.CONTAINER_APP }} \
            --resource-group ${{ vars.RESOURCE_GROUP }} \
            --image $ACR_SERVER/demo-g6:${{ github.sha }}

      - name: Verify deployment
        run: |
          FQDN=$(az containerapp show \
            --name ${{ vars.CONTAINER_APP }} \
            --resource-group ${{ vars.RESOURCE_GROUP }} \
            --query "properties.configuration.ingress.fqdn" -o tsv)
          for i in 1 2 3 4 5; do
            curl -sf "https://$FQDN" && exit 0
            echo "Attempt $i failed, retrying in 10s..."
            sleep 10
          done
          echo "Health check failed after 5 attempts!" && exit 1
```

---

### 2. UPPDATERA DOCKERFILE

#### Nuvarande Demo-G6 Dockerfile → Uppdaterad version
```dockerfile
# Demo-G6/Dockerfile
# Multi-stage build för optimal image storlek

# Build stage
FROM python:3.11-slim as builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim

# Installera ODBC driver för Azure SQL (om framtida behov)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gnupg2 unixodbc \
    && rm -rf /var/lib/apt/lists/*

# Om du använder Azure SQL framtidigt, uncomment detta:
# && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | \
#    gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
# && curl -fsSL https://packages.microsoft.com/config/debian/12/prod.list > \
#    /etc/apt/sources.list.d/mssql-release.list \
# && apt-get update \
# && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 \

WORKDIR /app

# Kopiera installerade packages från builder
COPY --from=builder /root/.local /root/.local

# Set environment variabler
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Kopiera application code
COPY . .

EXPOSE 5000

# Kör entrypoint script
CMD ["bash", "entrypoint.sh"]
```

---

### 3. SKAPA ENTRYPOINT SCRIPT

#### Ny fil: Demo-G6/entrypoint.sh
```bash
#!/bin/bash
set -e

# Färgad output för bättre läsning
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting Demo-G6 Application...${NC}"

# Kontrollera required environment variables
if [ -z "$FLASK_ENV" ]; then
    export FLASK_ENV=development
    echo -e "${YELLOW}FLASK_ENV not set, using: development${NC}"
fi

if [ -z "$DATABASE_URL" ]; then
    export DATABASE_URL="sqlite:///demo_g6.db"
    echo -e "${YELLOW}DATABASE_URL not set, using: SQLite${NC}"
fi

# Vänta på databas (om nätverksanslutning)
if [[ "$DATABASE_URL" == *"tcp"* ]] || [[ "$DATABASE_URL" == *"azure"* ]]; then
    echo -e "${YELLOW}Waiting for database to be ready...${NC}"
    max_attempts=30
    attempt=1
    while [ $attempt -le $max_attempts ]; do
        if python -c "from sqlalchemy import create_engine; engine = create_engine('$DATABASE_URL'); engine.execute('SELECT 1')" 2>/dev/null; then
            echo -e "${GREEN}Database is ready!${NC}"
            break
        fi
        echo -e "${YELLOW}Database not ready, attempt $attempt/$max_attempts. Retrying in 2s...${NC}"
        sleep 2
        attempt=$((attempt + 1))
    done
    
    if [ $attempt -gt $max_attempts ]; then
        echo -e "${RED}Database failed to become ready!${NC}"
        exit 1
    fi
fi

# Kör databas migrations
echo -e "${YELLOW}Running database migrations...${NC}"
if flask db upgrade > /dev/null 2>&1; then
    echo -e "${GREEN}Database migrations completed successfully${NC}"
else
    echo -e "${YELLOW}Database migrations skipped or already up-to-date${NC}"
fi

# Starta Gunicorn
echo -e "${YELLOW}Starting Gunicorn...${NC}"
echo -e "${GREEN}Application is running on port 5000${NC}"
exec gunicorn \
    --bind 0.0.0.0:5000 \
    --workers 2 \
    --worker-class sync \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    wsgi:app
```

**Gör scriptet executable:**
```bash
chmod +x /Users/ludwigsevenheim/Demo-G6/entrypoint.sh
```

---

### 4. UPPDATERA .DOCKERIGNORE

#### Ny fil: Demo-G6/.dockerignore
```
# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/
.Python
env/
venv/
ENV/

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Git
.git/
.gitignore
.gitattributes

# OS
.DS_Store
Thumbs.db

# Misc
.pytest_cache/
.coverage
htmlcov/
.tox/
.venv/
instance/

# Project specific
*.log
*.db
demo_g6.db
news_flash.db
```

---

### 5. SKAPA AZURE-CONFIG FIL

#### Ny fil: Demo-G6/.azure-config
```
# Azure Configuration for Demo-G6
# Notera: Dessa SKA inte commitas till Git! 
# I stället använd GitHub Environment Variables/Secrets

# Resursgruppsnamn i Azure
RESOURCE_GROUP=rg-demo-g6

# Azure Container Registry namn
ACR_NAME=acrdmg6

# Azure region
LOCATION=swedencentral

# Container App namn
CONTAINER_APP=ca-demo-g6

# Notering: Dessa är template-värden
# Faktiska värdena sätts via GitHub Secrets:
#   AZURE_CLIENT_ID
#   AZURE_TENANT_ID
#   AZURE_SUBSCRIPTION_ID
```

---

### 6. UPPDATERA REQUIREMENTS.TXT

#### Nuvarande Demo-G6/requirements.txt → Uppdaterad
```
# Web Framework
flask>=3.0.0

# Database & ORM
flask-sqlalchemy>=3.0.0
flask-migrate>=4.0.0

# Configuration
python-dotenv>=1.0.0

# Production Server
gunicorn==22.0.0

# Azure SQL Support (uncomment if using Azure SQL)
# pyodbc==5.2.0

# Debugging & Development (optional)
# flask-debugtoolbar>=0.14.0
# pytest>=7.0.0
# pytest-flask>=1.2.0
```

---

### 7. GITHUB REPOSITORY SECRETS/VARIABLES

#### Steg 1: Gå till Repository Settings
```
GitHub → Settings → Secrets and variables → Actions
```

#### Steg 2: Lägg till Environment Secrets (Environment: production)
```
AZURE_CLIENT_ID          = <your-client-id>
AZURE_TENANT_ID          = <your-tenant-id>
AZURE_SUBSCRIPTION_ID    = <your-subscription-id>
```

#### Steg 3: Lägg till Repository Variables
```
ACR_NAME       = acrdmg6
RESOURCE_GROUP = rg-demo-g6
CONTAINER_APP  = ca-demo-g6
```

**OBS:** Credentials bör inte commitas till repo!

---

### 8. AZURE SETUP SCRIPT (En gång)

```bash
#!/bin/bash
# Azure setup - kör detta en gång

# Variables
RESOURCE_GROUP="rg-demo-g6"
ACR_NAME="acrdmg6"
LOCATION="swedencentral"
CONTAINER_APP="ca-demo-g6"
SUBSCRIPTION_ID="<your-subscription-id>"

# Login to Azure
az login

# Set subscription
az account set --subscription $SUBSCRIPTION_ID

# Create Resource Group
echo "Creating Resource Group..."
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION

# Create Container Registry
echo "Creating Container Registry..."
az acr create \
    --resource-group $RESOURCE_GROUP \
    --name $ACR_NAME \
    --sku Basic

# Create Container App Environment
echo "Creating Container App Environment..."
az containerapp env create \
    --name demo-g6-env \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION

# Create Container App
echo "Creating Container App..."
az containerapp create \
    --name $CONTAINER_APP \
    --resource-group $RESOURCE_GROUP \
    --environment demo-g6-env \
    --image demog6placeholder:latest \
    --target-port 5000 \
    --ingress external \
    --query properties.configuration.ingress.fqdn

echo "Setup complete!"
echo "Now configure GitHub Secrets with the output from:"
echo "az acr credential show --name $ACR_NAME"
```

---

## VERIFIERING & TESTNING

### Lokal Docker Testing

#### Build Docker image
```bash
cd /Users/ludwigsevenheim/Demo-G6
docker build -t demo-g6:test .
```

#### Run Docker container lokalt
```bash
docker run -it -p 5000:5000 \
  -e FLASK_ENV=development \
  -e DATABASE_URL="sqlite:///demo_g6.db" \
  -v $(pwd):/app \
  demo-g6:test
```

#### Test endpoints
```bash
# I annan terminal:
curl http://localhost:5000/
curl http://localhost:5000/subscribe

# Verifiera migrations:
curl http://localhost:5000/

# Se logs:
docker logs <container-id>
```

---

### Databas Migrations Testning

#### Testa migrations lokalt
```bash
cd /Users/ludwigsevenheim/Demo-G6

# Aktivera venv
source .venv/bin/activate

# Initialisera databas (om första gången)
flask db init

# Skapa migration från models
flask db migrate -m "Initial migration"

# Verifiera migration file skapades
cat migrations/versions/*.py

# Applicera migration
flask db upgrade

# Verifiera databas
sqlite3 demo_g6.db ".tables"
```

---

## COMMON ISSUES & TROUBLESHOOTING

### Issue 1: Docker Build Fails
```bash
# Problem: "pip install failed"
# Solution:
docker build --no-cache -t demo-g6:test .

# Eller build med verbose output:
docker build --progress=plain -t demo-g6:test .
```

### Issue 2: Database Migration Errors
```bash
# Problem: "flask db upgrade fails"
# Solution 1: Check FLASK_ENV
echo $FLASK_ENV

# Solution 2: Backup existing db
mv demo_g6.db demo_g6.db.backup

# Solution 3: Initialize fresh
flask db init
flask db migrate -m "Initial"
flask db upgrade
```

### Issue 3: Container Fails to Start
```bash
# Check logs
docker logs <container-id>

# Common causes:
# 1. DATABASE_URL inte set
# 2. Port 5000 redan i användning
# 3. FLASK_ENV inte set

# Test locally:
FLASK_ENV=development DATABASE_URL="sqlite:///test.db" python wsgi.py
```

### Issue 4: Health Check Fails in Azure
```bash
# Azure portal → Container App → Console
# eller SSH in och kör:
curl http://localhost:5000/
```

---

## DEPLOYMENT WORKFLOW

### Lokal Development
```bash
# 1. Activate venv
source .venv/bin/activate

# 2. Set environment variables
export FLASK_ENV=development
export DATABASE_URL="sqlite:///demo_g6.db"

# 3. Run Flask
flask run

# 4. Access på http://localhost:5000
```

### Pre-Deployment Testing
```bash
# 1. Build Docker image
docker build -t demo-g6:pre-deploy .

# 2. Test image locally
docker run -it -p 5000:5000 \
  -e FLASK_ENV=production \
  -e DATABASE_URL="sqlite:///test.db" \
  demo-g6:pre-deploy

# 3. Verify endpoints
curl http://localhost:5000/
```

### Deployment to Azure
```bash
# 1. Push to GitHub
git add .
git commit -m "feat: Add CI/CD pipeline"
git push origin main

# 2. GitHub Actions automatiskt:
#    - Builds Docker image
#    - Pushes to ACR
#    - Deploys to Container App
#    - Runs health checks

# 3. Monitor deployment
az containerapp show \
  --name ca-demo-g6 \
  --resource-group rg-demo-g6 \
  --query properties.runningStatus

# 4. Get app URL
az containerapp show \
  --name ca-demo-g6 \
  --resource-group rg-demo-g6 \
  --query properties.configuration.ingress.fqdn
```

---

## ROLLBACK PLAN

### Om deployment misslyckas

#### Option 1: Git Revert
```bash
# Se previous version
git log --oneline

# Revert to previous commit
git revert <commit-hash>
git push

# GitHub Actions körs automatiskt med old version
```

#### Option 2: Manual Azure Rollback
```bash
# Get previous image from ACR
az acr repository list-tags \
  --name acrdmg6 \
  --repository demo-g6

# Update Container App to old image
az containerapp update \
  --name ca-demo-g6 \
  --resource-group rg-demo-g6 \
  --image acrdmg6.azurecr.io/demo-g6:<old-tag>
```

---

## SÄKERHET - CHECKLIST

- [ ] GitHub Secrets inte committade
- [ ] .azure-config inte committad (lägg till i .gitignore)
- [ ] DATABASE_URL säker (inte hardcoded)
- [ ] SECRET_KEY säker för production
- [ ] OIDC Federation konfigurerad (inte klassiska credentials)
- [ ] ACR är privat (inte public)
- [ ] Container App Ingress kräver authentication (om behövs)
- [ ] Regelbundna dependency updates (flask, gunicorn, etc)

---

## MONITORING & LOGGING

### Azure Logs
```bash
# Visa recent logs
az containerapp logs show \
  --name ca-demo-g6 \
  --resource-group rg-demo-g6 \
  --follow

# Eller i Azure Portal:
# Container App → Logs → Query
```

### Docker Logs (lokalt)
```bash
docker logs <container-id> --follow
docker logs <container-id> --tail 50
```

### Application Health
```bash
# Systemhälsa
curl https://<app-url>/health

# Databaskontroll
curl https://<app-url>/db-health

# Metrics
curl https://<app-url>/metrics
```

---

**Next Steps:**
1. ✅ Säkerställ Azure resurserna är skapade
2. ✅ Konfigurera GitHub Secrets
3. ✅ Kopiera och anpassa workflow
4. ✅ Test lokalt med Docker
5. ✅ Push till main och verifiera deployment

**Support Resources:**
- [Azure Container Apps Docs](https://learn.microsoft.com/en-us/azure/container-apps/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
