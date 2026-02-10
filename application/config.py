"""
Demo G6 - Application configuration using dataclasses.
"""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    """Base configuration."""

    # ÄNDRING 1: Hämta nyckeln från miljön, annars använd 'dev-key' om vi kör lokalt.
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-key")
    
    DEBUG: bool = False
    TESTING: bool = False
    
    # Explicitly use the root directory for SQLite database
    _root = str(Path(__file__).parent.parent)
    SQLALCHEMY_DATABASE_URI: str = f"sqlite:///{_root}/news_flash.db"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False


@dataclass
class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG: bool = True


@dataclass
class TestingConfig(Config):
    """Testing configuration."""
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"


@dataclass
class ProductionConfig(Config):
    """Production configuration."""
    
    # ÄNDRING 2: I produktion, hämta databas-adressen från molnleverantören
    # (Om ingen finns, fall tillbaka på SQLite, men varnar)
    SQLALCHEMY_DATABASE_URI: str = os.environ.get("DATABASE_URL", Config.SQLALCHEMY_DATABASE_URI)

    # ÄNDRING 3: Säkerhetsinställningar för Cookies (Kräver HTTPS)
    SESSION_COOKIE_SECURE: bool = True
    REMEMBER_COOKIE_SECURE: bool = True
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = 'Lax'


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}