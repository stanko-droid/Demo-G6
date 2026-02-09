from application.data.models.user import User

class AuthService:
    """
    Denna klass är 'Vakten'. Den sköter kontrollerna.
    """
    @staticmethod
    def login(email, password):
        # 1. Hämta användaren
        user = User.query.filter_by(email=email).first()
        
        # 2. Kolla lösenord
        if user and user.check_password(password):
            return user  # Godkänd!
            
        return None  # Nekad!