"""
Public routes - accessible without authentication.

This blueprint handles all public-facing pages including the landing page.
"""

from flask import Blueprint, render_template
from app.business.services import JokeService

bp = Blueprint("public", __name__)

# Initialize service
joke_service = JokeService()


@bp.route("/")
def index():
    """Render the landing page with a random joke."""
    jokes = joke_service.get_all_jokes()
    joke = joke_service.get_random_joke()
    return render_template("index.html", version="G6-SLAY-ULTIMATE", joke=joke, jokes=jokes)
