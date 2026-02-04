"""
Demo G6 - Application configuration using dataclasses.

Configuration is loaded from environment variables with sensible defaults
for development. In production, set SECRET_KEY to a secure random value.
"""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    """Base configuration."""

    SECRET_KEY: str = "dev-secret-key"
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

    pass


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


