"""
Public routes - accessible without authentication.

This blueprint handles all public-facing pages including the landing page
and subscription flow.
"""

from flask import Blueprint, render_template, request, jsonify
from sqlalchemy import text

from application import db
from application.business.services.subscription_service import SubscriptionService
from application.business.services import JokeService
from application.data.models.subscriber import Subscriber

bp = Blueprint("public", __name__)

# Initialize services
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
    email = request.form.get("email", "")
    name = request.form.get("name", "")

    # Use business layer for full subscription flow
    service = SubscriptionService()
    success, error = service.subscribe(email, name)

    if not success:
        # Return to form with error message, preserving input
        return render_template(
            "subscribe.html",
            error=error,
            email=email,
            name=name,
        )

    # Subscription saved successfully - show thank you page
    # Use normalized values for display
    normalized_email = service.normalize_email(email)
    normalized_name = service.normalize_name(name)

    return render_template(
        "thank_you.html",
        email=normalized_email,
        name=normalized_name,
    )


@bp.route("/subscribers")
def subscribers():
    """Display all subscribers in a table."""
    all_subscribers = db.session.query(Subscriber).order_by(
        Subscriber.subscribed_at.desc()
    ).all()
    
    return render_template(
        "subscribers.html",
        subscribers=all_subscribers,
        total_count=len(all_subscribers),
    )
