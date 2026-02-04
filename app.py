"""
Demo G6 - Main application entry point.

Uses application factory pattern from app module.
"""

from app import create_app

# Create app for both development and gunicorn production
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
