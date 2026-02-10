#!/bin/bash
set -e

# Environment variables should be injected by Container App
# DATABASE_URL, SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD are set via Azure secrets/env vars

# Verify critical environment variables are set
if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL environment variable not set!"
    exit 1
fi

if [ -z "$ADMIN_USERNAME" ] || [ -z "$ADMIN_PASSWORD" ]; then
    echo "ERROR: ADMIN_USERNAME and ADMIN_PASSWORD environment variables must be set!"
    exit 1
fi

# Set production environment
export FLASK_ENV=production

# Run database migrations
echo "✓ Running database migrations..."
flask db upgrade

echo "✓ Seeding admin user..."
flask create-admin "$ADMIN_USERNAME" "$ADMIN_PASSWORD"

echo "✓ Starting application with gunicorn..."
exec gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 wsgi:app
