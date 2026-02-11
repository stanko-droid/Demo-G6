from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_talisman import Talisman
import os

# Initiera databas och login-manager utanför funktionen
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(env=None):
    # Få absolut sökväg
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Använd de gamla platserna för templates och static
    app = Flask(
        __name__,
        template_folder=os.path.join(root_dir, 'templates'),
        static_folder=os.path.join(root_dir, 'static')
    )

    # --- KONFIGURATION ---
    # Miljöspecifik konfiguration
    if env == "production":
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_nyckel_hemlig')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    elif env == "testing":
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_secret_key'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
    else:
        app.config['DEBUG'] = True
        app.config['TESTING'] = False
        app.config['SECRET_KEY'] = 'dev_nyckel_hemlig'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Session security - only enforce HTTPS in production
    if env == "production":
        app.config['SESSION_COOKIE_SECURE'] = True
    else:
        app.config['SESSION_COOKIE_SECURE'] = False
    
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Initiera extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Talisman för security headers (only in production)
    if env == "production":
        Talisman(app)
    
    # Ställ in vart man skickas om man inte är inloggad
    login_manager.login_view = 'admin_bp.login'
    
    # User loader callback för Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from application.data.models.user import User
        return User.query.get(int(user_id))

    # Importera och registrera Blueprints
    from application.admin import admin_bp
    from application.presentation.routes.public import bp as public_bp
    # (Lägg till fler blueprints här om du har, t.ex. main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(public_bp)
    
    # Registrera CLI commands
    from application.commands import register_commands
    register_commands(app)

    # Security headers
    @app.after_request
    def set_security_headers(response):
        """Add OWASP-recommended security headers to all responses."""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Only set HSTS in production (requires HTTPS)
        if env == "production":
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        """Custom 404 error page."""
        from flask import render_template
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Custom 500 error page."""
        from flask import render_template
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # --- HÄR ÄR DEN MAGISKA LÖSNINGEN ---
    with app.app_context():
        # 1. Skapa alla tabeller (om de inte finns)
        db.create_all()

        # 2. Importera User här inne för att undvika krockar
        from application.data.models.user import User

        # 3. Kolla om admin-kontot saknas
        admin_email = "admin@test.se"
        existing_admin = User.query.filter_by(email=admin_email).first()

        if not existing_admin:
            print(f"⚠️  Varning: '{admin_email}' saknades i databasen.")
            print("⚙️  Skapar admin-användare automatiskt...")
            
            # Skapa användaren
            new_admin = User(email=admin_email)
            new_admin.set_password("hemligt123")  # Sätter lösenordet
            
            db.session.add(new_admin)
            db.session.commit()
            
            print(f"✅ KLART! Admin skapad. Logga in med: {admin_email} / hemligt123")
        else:
            print("ℹ️  Admin-konto finns redan. Startar appen...")

    return app