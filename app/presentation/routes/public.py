"""
Public routes - accessible without authentication.

This blueprint handles all public-facing pages including the landing page.
"""

from flask import Blueprint, render_template, request
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


@bp.route("/subscribe")
def subscribe():
    """Render the subscription form."""
    return render_template("subscribe.html")


@bp.route("/subscribe/confirm", methods=["POST"])
def subscribe_confirm():
    """Handle subscription form submission."""
    email = request.form.get("email")
    name = request.form.get("name", "Subscriber")

    # Verification: print to terminal (no persistence yet)
    print(f"New subscription: {email} ({name})")

    return render_template("thank_you.html", email=email, name=name)
