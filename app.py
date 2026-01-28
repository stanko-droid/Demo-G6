"""
Demo G6 - Main application entry point.

Uses application factory pattern from app module.
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)