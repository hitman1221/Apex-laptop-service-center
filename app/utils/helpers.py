"""General application helper functions."""

import re


def clean_text(value: str | None) -> str | None:
    """Trim text and collapse repeated whitespace."""

    if not value:
        return None

    cleaned_value = re.sub(r"\s+", " ", value).strip()

    return cleaned_value or None


def normalize_email(value: str | None) -> str | None:
    """Normalize an optional email address."""

    if not value:
        return None

    return value.strip().lower() or None


def normalize_phone(value: str | None) -> str:
    """Return digits only from a phone number."""

    return re.sub(r"\D", "", value or "")