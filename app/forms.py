"""Website forms."""

from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    Optional,
)

from app.utils.validators import (
    validate_indian_phone,
    validate_indian_pincode,
)


SERVICE_CHOICES = [
    ("", "Select a service"),
    ("Laptop Repair", "Laptop Repair"),
    ("Laptop Not Charging", "Laptop Not Charging"),
    ("Laptop Display Repair", "Laptop Display Repair"),
    ("Laptop Keyboard Repair", "Laptop Keyboard Repair"),
    ("Laptop Overheating Repair", "Laptop Overheating Repair"),
    (
        "Software and OS Repair",
        "Software and OS Repair",
    ),
    ("Laptop Port Repair", "Laptop Port Repair"),
    ("Laptop Speaker Repair", "Laptop Speaker Repair"),
    (
        "Laptop Unlocking Assistance",
        "Laptop Unlocking Assistance",
    ),
    ("Other Repair Requirement", "Other Repair Requirement"),
]


class EnquiryForm(FlaskForm):
    """Customer callback and service enquiry form."""

    name = StringField(
        "Full Name",
        validators=[
            DataRequired(message="Enter your full name."),
            Length(
                min=2,
                max=100,
                message="Name must contain 2 to 100 characters.",
            ),
        ],
        render_kw={
            "placeholder": "Enter your full name",
            "autocomplete": "name",
        },
    )

    phone = StringField(
        "Mobile Number",
        validators=[
            DataRequired(message="Enter your mobile number."),
            validate_indian_phone,
        ],
        render_kw={
            "placeholder": "Enter 10-digit mobile number",
            "autocomplete": "tel",
            "inputmode": "numeric",
            "maxlength": "10",
        },
    )

    email = EmailField(
        "Email Address",
        validators=[
            Optional(),
            Email(message="Enter a valid email address."),
            Length(max=255),
        ],
        render_kw={
            "placeholder": "Enter your email address (optional)",
            "autocomplete": "email",
        },
    )

    pincode = StringField(
        "PIN Code",
        validators=[
            DataRequired(message="Enter your PIN code."),
            validate_indian_pincode,
        ],
        render_kw={
            "placeholder": "Enter 6-digit PIN code",
            "autocomplete": "postal-code",
            "inputmode": "numeric",
            "maxlength": "6",
        },
    )

    service = SelectField(
        "Required Service",
        choices=SERVICE_CHOICES,
        validators=[Optional()],
    )

    message = TextAreaField(
        "Describe the Issue",
        validators=[
            Optional(),
            Length(
                max=1000,
                message="Message cannot exceed 1000 characters.",
            ),
        ],
        render_kw={
            "placeholder": (
                "Mention laptop brand, model and issue"
            ),
            "rows": "4",
        },
    )

    submit = SubmitField("Request a Callback")