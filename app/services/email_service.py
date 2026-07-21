"""Email service for enquiry notifications."""

from __future__ import annotations

import logging
from threading import Thread

# pyrefly: ignore [missing-import]
from flask import current_app, render_template
# pyrefly: ignore [missing-import]
from flask_mail import Message

from app import mail


logger = logging.getLogger(__name__)


def send_async_email(app, message) -> None:
    """Send an email asynchronously using the application context."""
    with app.app_context():
        try:
            mail.send(message)
            logger.info("Asynchronous email sent successfully.")
        except Exception:
            logger.exception("Failed to send email asynchronously.")


def send_admin_enquiry_email(enquiry) -> bool:
    """
    Send enquiry notification to business owner.
    """

    recipient = current_app.config.get(
        "ENQUIRY_RECIPIENT_EMAIL"
    )

    if not recipient:
        logger.warning(
            "ENQUIRY_RECIPIENT_EMAIL is not configured."
        )
        return False

    try:
        message = Message(
            subject=f"New Website Enquiry - {enquiry.service}",
            recipients=[recipient],
            sender=current_app.config["MAIL_DEFAULT_SENDER"],
        )

        message.html = render_template(
            "emails/admin_enquiry.html",
            enquiry=enquiry,
        )

        message.body = f"""
New Website Enquiry

Name: {enquiry.name}
Phone: {enquiry.phone}
Email: {enquiry.email or 'Not Provided'}
Service: {enquiry.service}

Message:
{enquiry.message}
"""

        app = current_app._get_current_object()
        Thread(
            target=send_async_email,
            args=(app, message),
        ).start()

        logger.info(
            "Admin enquiry email dispatch initiated in background thread."
        )
        return True

    except Exception:
        logger.exception(
            "Failed to initiate admin enquiry email thread."
        )
        return False


def send_customer_confirmation_email(enquiry) -> bool:
    """
    Send confirmation email to customer.
    """

    if (
        not enquiry.email
        or not current_app.config.get(
            "SEND_CUSTOMER_CONFIRMATION_EMAIL"
        )
    ):
        return False

    try:
        message = Message(
            subject="Thank you for contacting Apex Laptop Service Center",
            recipients=[enquiry.email],
            sender=current_app.config["MAIL_DEFAULT_SENDER"],
        )

        message.html = render_template(
            "emails/customer_confirmation.html",
            enquiry=enquiry,
        )

        message.body = f"""
Dear {enquiry.name},

Thank you for contacting Apex Laptop Service Center.

We have received your enquiry regarding:

{enquiry.service}

Our team will contact you shortly.

Regards,
Apex Laptop Service Center
"""

        app = current_app._get_current_object()
        Thread(
            target=send_async_email,
            args=(app, message),
        ).start()

        logger.info(
            "Customer confirmation email dispatch initiated in background thread."
        )
        return True

    except Exception:
        logger.exception(
            "Failed to initiate customer confirmation email thread."
        )
        return False