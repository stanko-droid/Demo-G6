from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initiera databas och login-manager utanför funktionen
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # --- KONFIGURATION ---
    # (Behåll dina egna inställningar om de skiljer sig)
    app.config['SECRET_KEY'] = 'dev_nyckel_hemlig'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initiera extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Ställ in vart man skickas om man inte är inloggad
    login_manager.login_view = 'admin_bp.login'

    # Importera och registrera Blueprints
    from application.admin import admin_bp
    from application.presentation.routes.public import bp as public_bp
    # (Lägg till fler blueprints här om du har, t.ex. main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(public_bp)

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