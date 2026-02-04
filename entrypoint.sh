#!/bin/bash
set -e

# Run database migrations
echo "Running database migrations..."
flask db upgrade

# Start gunicorn
echo "Starting application server..."
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 "app:create_app()"
