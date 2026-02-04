"""
Joke service - handles business logic for jokes.
"""

from application.data.repositories import JokeRepository


class JokeService:
    """Service for handling joke business logic."""

    def __init__(self):
        """Initialize the joke service with repository."""
        self.repository = JokeRepository()

    def get_random_joke(self) -> str:
        """Get a random joke."""
        return self.repository.get_random_joke()

    def get_all_jokes(self) -> list[str]:
        """Get all jokes."""
        return self.repository.get_all_jokes()

    def get_joke_count(self) -> int:
        """Get the total number of jokes."""
        return self.repository.get_joke_count()
