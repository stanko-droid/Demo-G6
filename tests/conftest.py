"""Pytest fixtures for the News Flash application tests."""

import pytest
from application import create_app, db as _db


@pytest.fixture
def app():
    """Create application instance for testing.

    Uses in-memory SQLite database that is created fresh for each test.
    """
    app = create_app("testing")

    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    """Create test client for making HTTP requests.

    The test client simulates a browser without running a real server.
    """
    return app.test_client()


@pytest.fixture
def authenticated_client(app, client):
    """Create a test client with an authenticated admin session.

    Creates an admin user and logs them in, returning a client
    that can access protected routes.
    """
    from application.services.auth_service import AuthService
    AuthService.create_user("testadmin@test.com", "testpassword123")

    client.post("/admin/login", data={
        "email": "testadmin@test.com",
        "password": "testpassword123",
    })
    return client


@pytest.fixture
def runner(app):
    """Create CLI test runner."""
    return app.test_cli_runner()
