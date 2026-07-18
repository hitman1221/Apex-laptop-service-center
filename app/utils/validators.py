"""Custom form validators."""

import re

from wtforms import ValidationError


INDIAN_PHONE_PATTERN = re.compile(r"^[6-9]\d{9}$")


def validate_indian_phone(_form, field) -> None:
    """Validate a 10-digit Indian mobile number."""

    phone = re.sub(r"\D", "", field.data or "")

    if phone.startswith("91") and len(phone) == 12:
        phone = phone[2:]

    if not INDIAN_PHONE_PATTERN.fullmatch(phone):
        raise ValidationError(
            "Enter a valid 10-digit Indian mobile number."
        )

    field.data = phone