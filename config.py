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


def env_to_bool(variable_name: str, default: str = "false") -> bool:
    """Convert an environment variable into a Boolean value."""

    return (
        os.getenv(variable_name, default)
        .strip()
        .lower()
        in {"true", "1", "yes", "on"}
    )


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
    # Store Owner / Admin Authentication
    # ------------------------------------------------------------------

    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "apex@123")

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
    WTF_CSRF_TIME_LIMIT = 7200

    # ------------------------------------------------------------------
    # Session and cookie settings
    # ------------------------------------------------------------------

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = env_to_bool(
        "SESSION_COOKIE_SECURE",
        "false",
    )

    # ------------------------------------------------------------------
    # Business information
    # ------------------------------------------------------------------

    BUSINESS_NAME = os.getenv(
        "BUSINESS_NAME",
        "Apex Laptop Service Center",
    )

    BUSINESS_PHONE = "7021161621"

    BUSINESS_WHATSAPP_NUMBER = "917021161621"

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
            "https://www.google.com/maps/search/"
            "?api=1&query=Apex+Laptop+Service+Center+Hanuman+Nagar+Kandivali+East"
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

    # ------------------------------------------------------------------
    # Transactional email
    # ------------------------------------------------------------------

    MAIL_SERVER = os.getenv(
        "MAIL_SERVER",
        "smtp-relay.brevo.com",
    )

    MAIL_PORT = int(
        os.getenv("MAIL_PORT", "587")
    )

    MAIL_USE_TLS = env_to_bool(
        "MAIL_USE_TLS",
        "true",
    )

    MAIL_USE_SSL = env_to_bool(
        "MAIL_USE_SSL",
        "false",
    )

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    MAIL_DEFAULT_SENDER_NAME = os.getenv(
        "MAIL_DEFAULT_SENDER_NAME",
        "Apex Laptop Service Center",
    )

    MAIL_DEFAULT_SENDER_EMAIL = os.getenv(
        "MAIL_DEFAULT_SENDER_EMAIL",
        "apexlaptopsolution@gmail.com",
    )

    
    MAIL_DEFAULT_SENDER = (
        MAIL_DEFAULT_SENDER_NAME,
        MAIL_DEFAULT_SENDER_EMAIL,
    )

    ENQUIRY_RECIPIENT_EMAIL = os.getenv(
        "ENQUIRY_RECIPIENT_EMAIL"
    )

    SEND_CUSTOMER_CONFIRMATION_EMAIL = env_to_bool(
        "SEND_CUSTOMER_CONFIRMATION_EMAIL",
        "true",
    )


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