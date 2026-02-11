"""Tests for the SubscriptionService business logic."""

import pytest

from application.business.services.subscription_service import SubscriptionService


class TestEmailValidation:
    """Test email validation rules."""

    def test_valid_email(self, app):
        """Standard email format is accepted."""
        service = SubscriptionService()
        is_valid, error = service.validate_email("user@example.com")
        assert is_valid is True
        assert error == ""

    def test_valid_email_with_dots(self, app):
        """Email with dots in local part is accepted."""
        service = SubscriptionService()
        is_valid, error = service.validate_email("first.last@example.com")
        assert is_valid is True

    def test_valid_email_with_plus(self, app):
        """Email with plus sign is accepted."""
        service = SubscriptionService()
        is_valid, error = service.validate_email("user+tag@example.com")
        assert is_valid is True

    def test_empty_email(self, app):
        """Empty string is rejected."""
        service = SubscriptionService()
        is_valid, error = service.validate_email("")
        assert is_valid is False
        assert "required" in error.lower()

    def test_whitespace_only_email(self, app):
        """Whitespace-only string is rejected."""
        service = SubscriptionService()
        is_valid, error = service.validate_email("   ")
        assert is_valid is False

    def test_no_at_sign(self, app):
        """Email without @ is rejected."""
        service = SubscriptionService()
        is_valid, error = service.validate_email("userexample.com")
        assert is_valid is False
        assert "invalid" in error.lower()

    def test_no_tld(self, app):
        """Email without TLD is rejected."""
        service = SubscriptionService()
        is_valid, error = service.validate_email("user@example")
        assert is_valid is False

    def test_double_at(self, app):
        """Email with double @ is rejected."""
        service = SubscriptionService()
        is_valid, error = service.validate_email("user@@example.com")
        assert is_valid is False


class TestEmailNormalization:
    """Test email normalization."""

    def test_lowercase_conversion(self, app):
        """Uppercase email is converted to lowercase."""
        service = SubscriptionService()
        assert service.normalize_email("USER@EXAMPLE.COM") == "user@example.com"

    def test_whitespace_stripped(self, app):
        """Leading and trailing whitespace is removed."""
        service = SubscriptionService()
        assert service.normalize_email("  user@example.com  ") == "user@example.com"

    def test_already_normalized(self, app):
        """Already-normalized email passes through unchanged."""
        service = SubscriptionService()
        assert service.normalize_email("user@example.com") == "user@example.com"


class TestNameNormalization:
    """Test name normalization."""

    def test_normal_name_trimmed(self, app):
        """Whitespace around name is stripped."""
        service = SubscriptionService()
        assert service.normalize_name("  John  ") == "John"

    def test_empty_name_defaults(self, app):
        """Empty string defaults to 'Subscriber'."""
        service = SubscriptionService()
        assert service.normalize_name("") == "Subscriber"

    def test_none_name_defaults(self, app):
        """None defaults to 'Subscriber'."""
        service = SubscriptionService()
        assert service.normalize_name(None) == "Subscriber"

    def test_whitespace_only_defaults(self, app):
        """Whitespace-only string defaults to 'Subscriber'."""
        service = SubscriptionService()
        assert service.normalize_name("   ") == "Subscriber"


class TestProcessSubscription:
    """Test the process_subscription method."""

    def test_valid_data_returns_dict(self, app):
        """Valid input returns a dictionary with processed data."""
        service = SubscriptionService()
        result = service.process_subscription("user@example.com", "John")
        assert isinstance(result, dict)
        assert result["email"] == "user@example.com"
        assert result["name"] == "John"

    def test_normalizes_email(self, app):
        """Email is normalized in the returned dictionary."""
        service = SubscriptionService()
        result = service.process_subscription("  USER@EXAMPLE.COM  ", "John")
        assert result["email"] == "user@example.com"

    def test_invalid_email_raises(self, app):
        """Invalid email raises ValueError."""
        service = SubscriptionService()
        with pytest.raises(ValueError):
            service.process_subscription("invalid", "John")

    def test_dict_has_expected_keys(self, app):
        """Returned dictionary contains all expected keys."""
        service = SubscriptionService()
        result = service.process_subscription("user@example.com", "John")
        assert "email" in result
        assert "name" in result
        assert "subscribed_at" in result
