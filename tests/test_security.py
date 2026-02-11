"""Tests for security features."""


class TestSecurityHeaders:
    """Test OWASP-recommended security headers."""

    def test_content_type_options(self, client):
        """X-Content-Type-Options header prevents MIME sniffing."""
        response = client.get("/")
        assert response.headers.get("X-Content-Type-Options") == "nosniff"

    def test_frame_options(self, client):
        """X-Frame-Options header prevents clickjacking."""
        response = client.get("/")
        assert response.headers.get("X-Frame-Options") == "SAMEORIGIN"

    def test_xss_protection(self, client):
        """X-XSS-Protection header enables browser XSS filter."""
        response = client.get("/")
        assert "1" in response.headers.get("X-XSS-Protection", "")

    def test_referrer_policy(self, client):
        """Referrer-Policy header is set."""
        response = client.get("/")
        assert response.headers.get("Referrer-Policy") is not None

    def test_no_hsts_in_testing(self, client):
        """HSTS header is NOT present in testing mode."""
        response = client.get("/")
        assert response.headers.get("Strict-Transport-Security") is None


class TestCSRFProtection:
    """Test CSRF token handling.

    Note: TestingConfig has WTF_CSRF_ENABLED = False for convenience.
    These tests document the CSRF behavior and explain the trade-off.
    """

    def test_csrf_disabled_in_testing(self, app):
        """CSRF is disabled in test configuration for convenience."""
        assert app.config.get("WTF_CSRF_ENABLED") is False

    def test_form_post_works_without_csrf_in_testing(self, client):
        """Form POST succeeds without CSRF token in testing mode."""
        response = client.post("/subscribe/confirm", data={
            "email": "test@example.com",
            "name": "Test User",
        })
        # Should succeed (200 or 302), not 400 (CSRF rejection)
        assert response.status_code in [200, 302]


class TestCreateAdminCLI:
    """Test the create-admin CLI command."""

    def test_create_admin_success(self, runner):
        """CLI creates admin user successfully."""
        result = runner.invoke(args=["create-admin", "admin@cli.com", "SecurePass1"])
        assert "created successfully" in result.output
        assert result.exit_code == 0

    def test_duplicate_username_idempotent(self, runner):
        """CLI handles existing username gracefully (idempotent)."""
        runner.invoke(args=["create-admin", "admin@cli.com", "SecurePass1"])
        result = runner.invoke(args=["create-admin", "admin@cli.com", "AnotherPass"])
        assert "already exists" in result.output
        assert result.exit_code == 0

    def test_short_password_rejected(self, runner):
        """CLI rejects password shorter than 8 characters."""
        result = runner.invoke(args=["create-admin", "admin@cli.com", "short"])
        assert "8 characters" in result.output
        assert result.exit_code == 1


class TestErrorPages:
    """Test custom error page rendering."""

    def test_404_returns_custom_page(self, client):
        """Non-existent route shows custom 404 page."""
        response = client.get("/this-page-does-not-exist")
        assert response.status_code == 404
        html = response.data.decode()
        assert "not found" in html.lower() or "404" in html or "hittades inte" in html.lower()

    def test_404_extends_base_template(self, client):
        """Custom 404 page uses the base template."""
        response = client.get("/this-page-does-not-exist")
        html = response.data.decode()
        # Should contain navigation from base.html or error template
        assert "Home" in html or "G6" in html or "<nav" in html or "startsidan" in html.lower()
