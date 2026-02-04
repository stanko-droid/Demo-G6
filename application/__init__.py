"""
Demo G6 - Application Factory

This module creates and configures the Flask application using the
application factory pattern. This pattern enables:
- Multiple instances with different configurations
- Easy testing with test configurations
- Delayed configuration loading
"""

import os
from pathlib import Path

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from .config import config

# Load .env file if it exists (for development)
_env_file = Path(__file__).parent.parent / ".env"
if _env_file.exists():
    load_dotenv(_env_file)

# Create extensions at module level (initialized in create_app)
db = SQLAlchemy()
migrate = Migrate()



def create_app(config_name: str | None = None) -> Flask:
    """
    Create and configure the Flask application.

    Args:
        config_name: Configuration to use ('development', 'testing', 'production').
                    Defaults to FLASK_ENV environment variable or 'development'.

    Returns:
        Configured Flask application instance.
    """
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    # ONLY load environment variables from secret files in PRODUCTION
    _root_path = Path(__file__).parent.parent
    if config_name == "production":
        _database_url_file = _root_path / ".database-url"
        _secret_key_file = _root_path / ".secret-key"
        
        if _database_url_file.exists():
            with open(_database_url_file) as f:
                os.environ["DATABASE_URL"] = f.read().strip()
        
        if _secret_key_file.exists():
            with open(_secret_key_file) as f:
                os.environ["SECRET_KEY"] = f.read().strip()

    app = Flask(
        __name__,
        template_folder="presentation/templates",
        static_folder="presentation/static",
    )

    # Load configuration
    app.config.from_object(config[config_name])
    
    # THEN: Override with environment variables if they exist (production only)
    if config_name == "production":
        if "DATABASE_URL" in os.environ:
            app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
        if "SECRET_KEY" in os.environ:
            app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models (after db.init_app to avoid circular imports)
    from .data import models  # noqa: F401
    
    # Register blueprints
    from .presentation.routes.public import bp as public_bp
    app.register_blueprint(public_bp)

    return app
