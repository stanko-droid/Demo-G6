"""Tests for protected routes and authentication flow."""


class TestUnauthenticatedAccess:
    """Test that protected routes redirect unauthenticated users."""

    def test_admin_dashboard_redirects(self, client):
        """Unauthenticated access to admin dashboard redirects to login."""
        response = client.get("/admin/dashboard")
        assert response.status_code == 302
        assert "/admin/login" in response.headers["Location"]

    def test_redirect_includes_next(self, client):
        """Redirect URL includes ?next parameter."""
        response = client.get("/admin/dashboard")
        assert "next" in response.headers["Location"]


class TestLoginFlow:
    """Test the login process."""

    def test_login_page_loads(self, client):
        """Login page renders successfully."""
        response = client.get("/admin/login")
        assert response.status_code == 200
        html = response.data.decode()
        assert "login" in html.lower() or "email" in html.lower()

    def test_login_page_has_form(self, client):
        """Login page contains a form."""
        response = client.get("/admin/login")
        html = response.data.decode()
        assert "<form" in html
        assert 'name="email"' in html or 'id="email"' in html
        assert 'name="password"' in html or 'id="password"' in html

    def test_valid_login_redirects(self, app, client):
        """Valid credentials redirect to admin."""
        from application.services.auth_service import AuthService
        AuthService.create_user("admin@test.com", "password123")
        response = client.post("/admin/login", data={
            "email": "admin@test.com",
            "password": "password123",
        })
        assert response.status_code == 302

    def test_invalid_login_stays_on_page(self, client):
        """Invalid credentials stay on login page."""
        response = client.post("/admin/login", data={
            "email": "wrong@test.com",
            "password": "wrong",
        })
        assert response.status_code == 200
        html = response.data.decode()
        assert "fel" in html.lower() or "invalid" in html.lower() or "error" in html.lower()


class TestAuthenticatedAccess:
    """Test that authenticated users can access protected routes."""

    def test_admin_dashboard_accessible(self, authenticated_client):
        """Authenticated user can view dashboard."""
        response = authenticated_client.get("/admin/dashboard")
        assert response.status_code == 200

    def test_admin_dashboard_content(self, authenticated_client):
        """Dashboard page has expected content."""
        response = authenticated_client.get("/admin/dashboard")
        html = response.data.decode()
        assert "subscriber" in html.lower() or "prenumerant" in html.lower()


class TestLogout:
    """Test the logout process."""

    def test_logout_redirects(self, authenticated_client):
        """Logout redirects to login page."""
        response = authenticated_client.get("/admin/logout")
        assert response.status_code == 302

    def test_admin_inaccessible_after_logout(self, authenticated_client):
        """After logout, admin routes redirect to login again."""
        authenticated_client.get("/admin/logout")
        response = authenticated_client.get("/admin/dashboard")
        assert response.status_code == 302
        assert "/admin/login" in response.headers["Location"]
