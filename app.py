"""
Demo G6 - Main application entry point for Flask.

This is the entry point for both:
- Development: flask run
- Production: gunicorn app:app
"""

from application import create_app

# Create the Flask application instance
app = create_app()

if __name__ == '__main__':
    # This runs when executing: python app.py
    # Flask CLI (flask run) ignores this block, so --port argument works
    app.run(debug=True, host='127.0.0.1', port=5000)

