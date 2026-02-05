#!/bin/bash
set -e

# Load environment variables from files if they exist
if [ -f ".database-url" ]; then
    export DATABASE_URL=$(cat .database-url)
    echo "✓ Database URL loaded"
fi

if [ -f ".secret-key" ]; then
    export SECRET_KEY=$(cat .secret-key)
    echo "✓ Secret key loaded"
fi

# Set production environment
export FLASK_ENV=production

# Run database migrations
echo "Running database migrations..."
flask db upgrade

# Start gunicorn
echo "Starting application server..."
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 "app:create_app()"
