"""Custom form validators."""

import re

from wtforms import ValidationError


INDIAN_PHONE_PATTERN = re.compile(r"^[6-9]\d{9}$")
PINCODE_PATTERN = re.compile(r"^[1-9]\d{5}$")


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


def validate_indian_pincode(_form, field) -> None:
    """Validate a six-digit Indian postal PIN code."""

    pincode = (field.data or "").strip()

    if not PINCODE_PATTERN.fullmatch(pincode):
        raise ValidationError(
            "Enter a valid 6-digit PIN code."
        )

    field.data = pincode