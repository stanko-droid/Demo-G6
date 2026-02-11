"""Integration tests for the complete subscription flow.

These tests exercise all three layers: presentation (routes),
business (service), and data (repository + database).
"""

from application.data.models.subscriber import Subscriber


class TestSuccessfulSubscription:
    """Test the happy path for form submission."""

    def test_valid_submission_redirects(self, client):
        """Valid form data results in success page or redirect."""
        response = client.post("/subscribe/confirm", data={
            "email": "test@example.com",
            "name": "Test User",
        })
        # May redirect (302) or render directly (200)
        assert response.status_code in [200, 302]

    def test_valid_submission_saves_to_database(self, app, client):
        """Valid submission persists subscriber to database."""
        client.post("/subscribe/confirm", data={
            "email": "test@example.com",
            "name": "Test User",
        })
        subscriber = Subscriber.query.filter_by(email="test@example.com").first()
        assert subscriber is not None
        assert subscriber.name == "Test User"

    def test_thank_you_page_content(self, client):
        """Successful subscription shows confirmation."""
        response = client.post("/subscribe/confirm", data={
            "email": "test@example.com",
            "name": "Test User",
        }, follow_redirects=True)
        html = response.data.decode()
        assert "test@example.com" in html or "thank" in html.lower()


class TestValidationErrors:
    """Test that invalid form data is handled correctly."""

    def test_empty_email_shows_error(self, client):
        """Submitting empty email returns to form with error."""
        response = client.post("/subscribe/confirm", data={
            "email": "",
            "name": "Test User",
        })
        html = response.data.decode()
        assert response.status_code == 200
        # Should stay on form page with error message
        assert "required" in html.lower() or "invalid" in html.lower() or "error" in html.lower()

    def test_invalid_email_shows_error(self, client):
        """Submitting invalid email format shows error message."""
        response = client.post("/subscribe/confirm", data={
            "email": "not-an-email",
            "name": "Test User",
        })
        html = response.data.decode()
        assert response.status_code == 200
        assert "invalid" in html.lower() or "email" in html.lower()

    def test_invalid_email_not_saved(self, app, client):
        """Invalid email does not create a database record."""
        client.post("/subscribe/confirm", data={
            "email": "not-an-email",
            "name": "Test User",
        })
        count = Subscriber.query.count()
        assert count == 0


class TestDuplicatePrevention:
    """Test that duplicate emails are rejected."""

    def test_duplicate_email_shows_error(self, app, client):
        """Submitting an already-subscribed email shows error."""
        # First subscription succeeds
        client.post("/subscribe/confirm", data={
            "email": "test@example.com",
            "name": "First User",
        })
        # Second with same email fails
        response = client.post("/subscribe/confirm", data={
            "email": "test@example.com",
            "name": "Second User",
        }, follow_redirects=True)
        html = response.data.decode()
        assert "already" in html.lower() or "subscribed" in html.lower() or "error" in html.lower()

    def test_duplicate_only_saves_once(self, app, client):
        """Duplicate submission doesn't create second record."""
        client.post("/subscribe/confirm", data={
            "email": "test@example.com",
            "name": "First User",
        })
        client.post("/subscribe/confirm", data={
            "email": "test@example.com",
            "name": "Second User",
        })
        count = Subscriber.query.filter_by(email="test@example.com").count()
        assert count == 1


class TestNormalizationIntegration:
    """Test that data normalization works through the full stack."""

    def test_email_normalized_in_database(self, app, client):
        """Uppercase email is stored as lowercase."""
        client.post("/subscribe/confirm", data={
            "email": "  TEST@EXAMPLE.COM  ",
            "name": "Test User",
        })
        subscriber = Subscriber.query.first()
        assert subscriber is not None
        assert subscriber.email == "test@example.com"

    def test_name_normalized_in_database(self, app, client):
        """Name is trimmed in database."""
        client.post("/subscribe/confirm", data={
            "email": "test@example.com",
            "name": "  Jane Doe  ",
        })
        subscriber = Subscriber.query.first()
        assert subscriber.name == "Jane Doe"

    def test_empty_name_gets_default(self, app, client):
        """Empty name defaults to 'Subscriber'."""
        client.post("/subscribe/confirm", data={
            "email": "test@example.com",
            "name": "",
        })
        subscriber = Subscriber.query.first()
        assert subscriber.name == "Subscriber"
