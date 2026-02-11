"""Tests for the AuthService authentication logic."""

import pytest
from application.services.auth_service import AuthService, DuplicateUsernameError


class TestCreateUser:
    """Test user creation through AuthService."""

    def test_create_user_returns_user(self, app):
        """create_user() returns a User instance."""
        user = AuthService.create_user("admin@test.com", "password123")
        assert user is not None
        assert user.email == "admin@test.com"

    def test_password_is_hashed(self, app):
        """Stored password is not plain text."""
        user = AuthService.create_user("admin@test.com", "password123")
        assert user.password_hash != "password123"
        assert len(user.password_hash) > 50

    def test_duplicate_username_raises_error(self, app):
        """Creating user with existing email raises DuplicateUsernameError."""
        AuthService.create_user("admin@test.com", "password123")
        with pytest.raises(DuplicateUsernameError):
            AuthService.create_user("admin@test.com", "different_password")


class TestAuthenticate:
    """Test credential verification."""

    def test_correct_credentials(self, app):
        """Valid credentials return User."""
        AuthService.create_user("admin@test.com", "password123")
        user = AuthService.authenticate("admin@test.com", "password123")
        assert user is not None
        assert user.email == "admin@test.com"

    def test_wrong_password(self, app):
        """Wrong password returns None."""
        AuthService.create_user("admin@test.com", "password123")
        result = AuthService.authenticate("admin@test.com", "wrongpassword")
        assert result is None

    def test_nonexistent_username(self, app):
        """Non-existent email returns None."""
        result = AuthService.authenticate("nobody@test.com", "password123")
        assert result is None


class TestInactiveUsers:
    """Test that inactive users cannot authenticate."""

    def test_inactive_user_returns_none(self, app):
        """Inactive user cannot authenticate even with correct password."""
        from application import db
        user = AuthService.create_user("admin@test.com", "password123")
        user.is_active = False
        db.session.commit()
        result = AuthService.authenticate("admin@test.com", "password123")
        assert result is None


class TestPasswordHashing:
    """Test password hash behavior."""

    def test_check_password_correct(self, app):
        """check_password() returns True for correct password."""
        user = AuthService.create_user("admin@test.com", "password123")
        assert user.check_password("password123") is True

    def test_check_password_wrong(self, app):
        """check_password() returns False for wrong password."""
        user = AuthService.create_user("admin@test.com", "password123")
        assert user.check_password("wrongpassword") is False

    def test_different_users_different_hashes(self, app):
        """Same password produces different hashes for different users."""
        user1 = AuthService.create_user("admin1@test.com", "samepassword")
        user2 = AuthService.create_user("admin2@test.com", "samepassword")
        assert user1.password_hash != user2.password_hash
