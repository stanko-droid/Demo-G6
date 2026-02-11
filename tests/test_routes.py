"""Tests for public routes and page content."""


class TestPublicRoutes:
    """Test that public pages load correctly."""

    def test_index_returns_200(self, client):
        """Home page loads successfully."""
        response = client.get("/")
        assert response.status_code == 200

    def test_subscribe_returns_200(self, client):
        """Subscribe page loads successfully."""
        response = client.get("/subscribe")
        assert response.status_code == 200

    def test_unknown_route_returns_404(self, client):
        """Non-existent routes return 404."""
        response = client.get("/does-not-exist")
        assert response.status_code == 404


class TestPageContent:
    """Test that pages contain expected content."""

    def test_index_contains_title(self, client):
        """Home page shows the application name."""
        response = client.get("/")
        html = response.data.decode()
        assert "G6" in html

    def test_subscribe_contains_heading(self, client):
        """Subscribe page has a heading."""
        response = client.get("/subscribe")
        html = response.data.decode()
        assert "Subscribe" in html

    def test_subscribe_contains_email_input(self, client):
        """Subscribe page has an email input field."""
        response = client.get("/subscribe")
        html = response.data.decode()
        assert 'name="email"' in html


class TestSubscribeForm:
    """Test the subscription form elements."""

    def test_form_has_action(self, client):
        """Form posts to the confirm endpoint."""
        response = client.get("/subscribe")
        html = response.data.decode()
        assert "<form" in html
        assert "/subscribe/confirm" in html

    def test_form_has_email_field(self, client):
        """Form includes email input."""
        response = client.get("/subscribe")
        html = response.data.decode()
        assert 'name="email"' in html

    def test_form_has_submit_button(self, client):
        """Form has a submit button."""
        response = client.get("/subscribe")
        html = response.data.decode()
        assert "type=\"submit\"" in html or "Submit" in html or "Subscribe" in html

    def test_form_method_is_post(self, client):
        """Form uses POST method."""
        response = client.get("/subscribe")
        html = response.data.decode()
        assert 'method="POST"' in html or 'method="post"' in html
