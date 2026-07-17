"""Flask application factory."""

import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import CONFIG_MAP


db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_name: str | None = None) -> Flask:
    """Create and configure the Flask application."""

    selected_config = (
        config_name
        or os.getenv("FLASK_ENV")
        or "default"
    )

    app = Flask(__name__)
    app.config.from_object(
        CONFIG_MAP.get(selected_config, CONFIG_MAP["default"])
    )

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from app.routes import main_bp

    app.register_blueprint(main_bp)

    register_template_context(app)

    return app


def register_template_context(app: Flask) -> None:
    """Expose common business values to Jinja templates."""

    @app.context_processor
    def inject_business_details() -> dict:
        return {
            "business": {
                "name": app.config["BUSINESS_NAME"],
                "phone": app.config["BUSINESS_PHONE"],
                "email": app.config["BUSINESS_EMAIL"],
                "address": app.config["BUSINESS_ADDRESS"],
                "hours": app.config["BUSINESS_HOURS"],
                "experience": app.config["BUSINESS_EXPERIENCE"],
                "rating": app.config["BUSINESS_RATING"],
                "review_count": app.config[
                    "BUSINESS_REVIEW_COUNT"
                ],
                "latitude": app.config["LATITUDE"],
                "longitude": app.config["LONGITUDE"],
                "maps_url": app.config["GOOGLE_MAPS_URL"],
                "whatsapp_number": app.config[
                    "WHATSAPP_NUMBER"
                ],
            }
        }