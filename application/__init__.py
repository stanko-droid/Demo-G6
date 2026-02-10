"""
Demo G6 - Application Factory
"""
import os
from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_talisman import Talisman  # <--- SÄKERHET
from dotenv import load_dotenv

from .config import config

# Ladda .env om den finns
_env_file = Path(__file__).parent.parent / ".env"
if _env_file.exists():
    load_dotenv(_env_file)

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name: str | None = None) -> Flask:
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(
        __name__,
        template_folder="presentation/templates",
        static_folder="presentation/static",
    )

    # --- DATABAS-KONFIGURATION ---
    basedir = os.path.abspath(os.path.dirname(__file__))
    root_dir = os.path.dirname(basedir)
    db_path = os.path.join(root_dir, 'news_flash.db')

    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    
    print(f"\n---> KOPPLAR TILL DATABAS PÅ: {db_path}\n")

    # --- INITIERA TILLÄGG ---
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Initiera Login-systemet
    login_manager.init_app(app)
    login_manager.login_view = 'admin_bp.login' 

    # Initiera Talisman (Säkerhet)
    # force_https=False är viktigt när vi kör lokalt (127.0.0.1)
    # content_security_policy=None tillåter oss använda enkel CSS/JS för nu
    Talisman(app, force_https=False, content_security_policy=None)

    # --- MODELLER & USER LOADER ---
    from .data import models  # noqa: F401
    from application.data.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # --- REGISTRERA BLUEPRINTS ---
    from .presentation.routes.public import bp as public_bp
    app.register_blueprint(public_bp)

    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    # --- REGISTRERA CLI-KOMMANDON (NYTT!) ---
    # Detta gör att 'flask create-admin' fungerar i terminalen
    from .commands import create_admin_command
    app.cli.add_command(create_admin_command)

    return app