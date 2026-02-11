from application.data.models.user import User
from application import db


class DuplicateUsernameError(Exception):
    """Raised when attempting to create a user with an existing email."""
    pass


class AuthService:
    """
    Denna klass är 'Vakten'. Den sköter kontrollerna.
    """
    @staticmethod
    def login(email, password):
        """Legacy method - use authenticate() instead."""
        # 1. Hämta användaren
        user = User.query.filter_by(email=email).first()
        
        # 2. Kolla lösenord
        if user and user.check_password(password):
            return user  # Godkänd!
            
        return None  # Nekad!
    
    @staticmethod
    def authenticate(email, password):
        """
        Authenticate a user with email and password.
        
        Returns User if credentials valid and user is active, None otherwise.
        This prevents username enumeration by returning None for both
        wrong password and non-existent user.
        """
        user = User.query.filter_by(email=email).first()
        
        # Return None if user doesn't exist
        if not user:
            return None
        
        # Return None if password is wrong
        if not user.check_password(password):
            return None
        
        # Return None if user is inactive
        if not user.is_active:
            return None
        
        return user
    
    @staticmethod
    def create_user(email, password):
        """
        Create a new user with hashed password.
        
        Args:
            email: User's email address
            password: Plain text password (will be hashed)
        
        Returns:
            User instance
        
        Raises:
            DuplicateUsernameError: If email already exists
        """
        # Check if user already exists
        existing = User.query.filter_by(email=email).first()
        if existing:
            raise DuplicateUsernameError(f"User with email '{email}' already exists")
        
        # Create new user
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Retrieve a user by their ID.
        
        Args:
            user_id: Integer user ID
        
        Returns:
            User instance or None if not found
        """
        return User.query.get(user_id)