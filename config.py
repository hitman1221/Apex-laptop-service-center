"""Application configuration."""

import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def normalize_database_url(database_url: str | None) -> str:
    """Normalize PostgreSQL URLs provided by hosting platforms."""

    if not database_url:
        return (
            "postgresql+psycopg2://apex_service_user:"
            "your_database_password@localhost:5432/apex_service_db"
        )

    if database_url.startswith("postgres://"):
        return database_url.replace(
            "postgres://",
            "postgresql+psycopg2://",
            1,
        )

    if database_url.startswith("postgresql://"):
        return database_url.replace(
            "postgresql://",
            "postgresql+psycopg2://",
            1,
        )

    return database_url


class Config:
    """Base application configuration."""

    # ------------------------------------------------------------------
    # Core application settings
    # ------------------------------------------------------------------

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "change-this-in-production",
    )

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------

    SQLALCHEMY_DATABASE_URI = normalize_database_url(
        os.getenv("DATABASE_URL")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }

    # ------------------------------------------------------------------
    # CSRF protection
    # ------------------------------------------------------------------

    WTF_CSRF_ENABLED = True

    # Time must be supplied in seconds.
    # 7200 seconds = 2 hours.
    WTF_CSRF_TIME_LIMIT = 7200

    # ------------------------------------------------------------------
    # Session and cookie settings
    # ------------------------------------------------------------------

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_SECURE = (
        os.getenv("SESSION_COOKIE_SECURE", "false").lower()
        == "true"
    )

    # ------------------------------------------------------------------
    # Business information
    # ------------------------------------------------------------------

    BUSINESS_NAME = os.getenv(
        "BUSINESS_NAME",
        "Apex Laptop Service Center",
    )

    BUSINESS_PHONE = os.getenv(
        "BUSINESS_PHONE",
        "08460450742",
    )

    BUSINESS_WHATSAPP_NUMBER = os.getenv(
        "BUSINESS_WHATSAPP_NUMBER",
        "917021161621",
    )

    BUSINESS_EMAIL = os.getenv(
        "BUSINESS_EMAIL",
        "apexlaptopsolution@gmail.com",
    )

    BUSINESS_ADDRESS = os.getenv(
        "BUSINESS_ADDRESS",
        (
            "101, Shree Samarth CHSL, Hanuman Nagar, "
            "Mahindra Yellow Gate, Akurli Road, "
            "Kandivali East, Mumbai - 400101"
        ),
    )

    BUSINESS_HOURS = os.getenv(
        "BUSINESS_HOURS",
        "Daily, 9:00 AM - 8:00 PM",
    )

    BUSINESS_EXPERIENCE = os.getenv(
        "BUSINESS_EXPERIENCE",
        "10 Years in Business",
    )

    BUSINESS_RATING = os.getenv(
        "BUSINESS_RATING",
        "4.7",
    )

    BUSINESS_REVIEW_COUNT = os.getenv(
        "BUSINESS_REVIEW_COUNT",
        "25",
    )

    # ------------------------------------------------------------------
    # Google Maps
    # ------------------------------------------------------------------

    LATITUDE = os.getenv(
        "LATITUDE",
        "19.200944",
    )

    LONGITUDE = os.getenv(
        "LONGITUDE",
        "72.865778",
    )

    GOOGLE_MAPS_URL = os.getenv(
        "GOOGLE_MAPS_URL",
        (
            "https://maps.app.goo.gl/"
            "JJrMb7CbNRCX5PVAA?g_st=ac"
        ),
    )

    GOOGLE_MAPS_EMBED_URL = os.getenv(
        "GOOGLE_MAPS_EMBED_URL",
        (
            "https://maps.google.com/maps?"
            "q=19.200944,72.865778"
            "&z=17"
            "&output=embed"
        ),
    )

    # ------------------------------------------------------------------
    # Upload limits
    # ------------------------------------------------------------------

    MAX_CONTENT_LENGTH = 2 * 1024 * 1024


class DevelopmentConfig(Config):
    """Local development configuration."""

    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    SESSION_COOKIE_SECURE = True


CONFIG_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}