"""Tests for the SubscriberRepository data access layer."""

from application.data.repositories.subscriber_repository import SubscriberRepository
from application.data.models.subscriber import Subscriber


class TestCreateSubscriber:
    """Test creating new subscribers."""

    def test_create_returns_subscriber(self, app):
        """create() returns a Subscriber instance."""
        repo = SubscriberRepository()
        subscriber = repo.create(email="test@example.com", name="Test User")
        assert isinstance(subscriber, Subscriber)

    def test_create_sets_fields(self, app):
        """Created subscriber has correct field values."""
        repo = SubscriberRepository()
        subscriber = repo.create(email="test@example.com", name="Test User")
        assert subscriber.email == "test@example.com"
        assert subscriber.name == "Test User"

    def test_create_sets_id(self, app):
        """Created subscriber gets an auto-generated ID."""
        repo = SubscriberRepository()
        subscriber = repo.create(email="test@example.com", name="Test User")
        assert subscriber.id is not None
        assert subscriber.id > 0

    def test_create_sets_timestamp(self, app):
        """Created subscriber gets an automatic timestamp."""
        repo = SubscriberRepository()
        subscriber = repo.create(email="test@example.com", name="Test User")
        assert subscriber.subscribed_at is not None


class TestFindSubscriber:
    """Test querying for subscribers."""

    def test_find_by_email_existing(self, app):
        """find_by_email() returns subscriber when email exists."""
        repo = SubscriberRepository()
        repo.create(email="test@example.com", name="Test User")
        found = repo.find_by_email("test@example.com")
        assert found is not None
        assert found.email == "test@example.com"

    def test_find_by_email_nonexistent(self, app):
        """find_by_email() returns None for unknown email."""
        repo = SubscriberRepository()
        found = repo.find_by_email("nobody@example.com")
        assert found is None

    def test_find_by_email_case_insensitive(self, app):
        """find_by_email() matches case-insensitively."""
        repo = SubscriberRepository()
        repo.create(email="test@example.com", name="Test User")
        found = repo.find_by_email("TEST@EXAMPLE.COM")
        assert found is not None


class TestDuplicateDetection:
    """Test duplicate subscriber prevention."""

    def test_exists_false_for_new_email(self, app):
        """exists() returns False for unknown email."""
        repo = SubscriberRepository()
        assert repo.exists("new@example.com") is False

    def test_exists_true_for_existing_email(self, app):
        """exists() returns True after subscriber is created."""
        repo = SubscriberRepository()
        repo.create(email="test@example.com", name="Test User")
        assert repo.exists("test@example.com") is True

    def test_create_duplicate_raises_error(self, app):
        """Creating subscriber with existing email raises IntegrityError."""
        from sqlalchemy.exc import IntegrityError
        import pytest

        repo = SubscriberRepository()
        repo.create(email="test@example.com", name="Test User")
        with pytest.raises(IntegrityError):
            repo.create(email="test@example.com", name="Another User")


class TestGetAll:
    """Test retrieving all subscribers."""

    def test_empty_database_returns_empty_list(self, app):
        """get_all() returns empty list when no subscribers exist."""
        repo = SubscriberRepository()
        result = repo.get_all()
        assert result == []

    def test_returns_all_subscribers(self, app):
        """get_all() returns all created subscribers."""
        repo = SubscriberRepository()
        repo.create(email="first@example.com", name="First")
        repo.create(email="second@example.com", name="Second")
        result = repo.get_all()
        assert len(result) == 2

    def test_ordered_newest_first(self, app):
        """get_all() returns subscribers with newest first."""
        repo = SubscriberRepository()
        repo.create(email="first@example.com", name="First")
        repo.create(email="second@example.com", name="Second")
        result = repo.get_all()
        # Second subscriber was created last, should be first in list
        assert result[0].email == "second@example.com"
        assert result[1].email == "first@example.com"

    def test_database_starts_empty(self, app):
        """Each test gets a fresh, empty database."""
        repo = SubscriberRepository()
        assert repo.get_all() == []
