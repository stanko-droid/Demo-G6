"""Smoke tests to verify basic application setup."""


def test_app_exists(app):
    """Verify the application instance is created."""
    assert app is not None


def test_app_is_testing(app):
    """Verify the app is using the testing configuration."""
    assert app.config["TESTING"] is True


def test_index_page_loads(client):
    """Verify the home page returns HTTP 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_nonexistent_page_returns_404(client):
    """Verify unknown routes return 404."""
    response = client.get("/nonexistent-page")
    assert response.status_code == 404
