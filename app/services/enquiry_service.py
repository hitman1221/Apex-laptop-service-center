"""Service layer for customer enquiries."""

from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models import Enquiry
from app.utils.helpers import clean_text, normalize_email


class EnquiryServiceError(Exception):
    """Raised when an enquiry cannot be created."""


class EnquiryService:
    """Handle enquiry-related business logic."""

    @staticmethod
    def create_enquiry(
        *,
        name: str,
        phone: str,
        email: str | None,
        pincode: str,
        service: str | None,
        message: str | None,
        source_page: str,
    ) -> Enquiry:
        """Validate, create and persist an enquiry."""

        enquiry = Enquiry(
            name=clean_text(name),
            phone=phone,
            email=normalize_email(email),
            pincode=pincode,
            service=clean_text(service),
            message=clean_text(message),
            source_page=source_page,
        )

        try:
            db.session.add(enquiry)
            db.session.commit()

        except SQLAlchemyError as exc:
            db.session.rollback()

            current_app.logger.exception(
                "Database error while saving an enquiry."
            )

            raise EnquiryServiceError(
                "Unable to save the enquiry."
            ) from exc

        return enquiry