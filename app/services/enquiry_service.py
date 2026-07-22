"""Service layer for customer enquiries."""

from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models import Enquiry
from app.services.email_service import (
    send_admin_enquiry_email,
    send_customer_confirmation_email,
)
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
        service: str,
        message: str,
        source_page: str,
    ) -> Enquiry:
        """
        Validate, create and persist a customer enquiry.

        Email notifications are attempted only after the enquiry has
        been successfully saved. An email failure does not remove or
        roll back the saved database record.
        """

        enquiry = Enquiry(
            name=clean_text(name),
            phone=clean_text(phone),
            email=normalize_email(email),
            service=clean_text(service),
            message=clean_text(message),
            source_page=clean_text(source_page),
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

        EnquiryService._send_email_notifications(enquiry)

        return enquiry

    @staticmethod
    def _send_email_notifications(enquiry: Enquiry) -> None:
        """
        Send admin and customer email notifications.

        Email service functions handle their own exceptions and return
        a Boolean status, keeping email failures separate from database
        persistence.
        """

        admin_email_sent = send_admin_enquiry_email(enquiry)

        if not admin_email_sent:
            current_app.logger.warning(
                "Admin notification email was not sent "
                "for enquiry ID %s.",
                enquiry.id,
            )

        if not enquiry.email:
            current_app.logger.info(
                "Customer confirmation email skipped because no "
                "customer email was provided for enquiry ID %s.",
                enquiry.id,
            )
            return

        customer_email_sent = send_customer_confirmation_email(
            enquiry
        )

        if not customer_email_sent:
            current_app.logger.warning(
                "Customer confirmation email was not sent "
                "for enquiry ID %s.",
                enquiry.id,
            )

    @staticmethod
    def get_all_enquiries(status: str | None = None) -> list[Enquiry]:
        """Fetch all customer enquiries, optionally filtered by status."""
        query = Enquiry.query

        if status and status.lower() != "all":
            query = query.filter_by(status=status.lower())

        return query.order_by(Enquiry.created_at.desc()).all()

    @staticmethod
    def get_enquiry_stats() -> dict[str, int]:
        """Compute status counts for the admin dashboard."""
        return {
            "total": Enquiry.query.count(),
            "new": Enquiry.query.filter_by(status="new").count(),
            "in_progress": Enquiry.query.filter_by(
                status="in_progress"
            ).count(),
            "completed": Enquiry.query.filter_by(
                status="completed"
            ).count(),
        }

    @staticmethod
    def update_enquiry_status(
        enquiry_id: int, new_status: str
    ) -> Enquiry | None:
        """Update the status of a specific customer enquiry."""
        enquiry = db.session.get(Enquiry, enquiry_id)
        if not enquiry:
            return None

        allowed_statuses = {"new", "in_progress", "completed"}
        if new_status.lower() in allowed_statuses:
            enquiry.status = new_status.lower()
            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                current_app.logger.exception(
                    "Error updating status for enquiry %s.", enquiry_id
                )
                raise EnquiryServiceError("Database update failed.")
        return enquiry