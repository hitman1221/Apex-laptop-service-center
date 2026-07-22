"""Website forms."""

from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional,
)

from app.utils.validators import validate_indian_phone


SERVICE_CHOICES = [
    ("", "Select a service"),
    ("Laptop Repair", "Laptop Repair"),
    ("Laptop Not Charging", "Laptop Not Charging"),
    ("Laptop Display Repair", "Laptop Display Repair"),
    ("Laptop Keyboard Repair", "Laptop Keyboard Repair"),
    (
        "Laptop Overheating Repair",
        "Laptop Overheating Repair",
    ),
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
    (
        "Other Repair Requirement",
        "Other Repair Requirement",
    ),
]


class EnquiryForm(FlaskForm):
    """Customer callback and service enquiry form."""

    name = StringField(
        "Full Name",
        validators=[
            DataRequired(
                message="Please enter your full name."
            ),
            Length(
                min=2,
                max=100,
                message=(
                    "Full name must contain "
                    "2 to 100 characters."
                ),
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
            DataRequired(
                message="Please enter your mobile number."
            ),
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
            Email(
                message="Please enter a valid email address."
            ),
            Length(
                max=255,
                message=(
                    "Email address cannot exceed "
                    "255 characters."
                ),
            ),
        ],
        render_kw={
            "placeholder": (
                "Enter your email address (optional)"
            ),
            "autocomplete": "email",
        },
    )

    service = SelectField(
        "Required Service",
        choices=SERVICE_CHOICES,
        validators=[
            DataRequired(
                message="Please select the required service."
            )
        ],
    )

    message = TextAreaField(
        "Describe the Issue",
        validators=[
            DataRequired(
                message="Please describe your laptop issue."
            ),
            Length(
                min=10,
                max=1000,
                message=(
                    "Issue description must contain "
                    "10 to 1000 characters."
                ),
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


class AdminLoginForm(FlaskForm):
    """Store Owner Admin Login Form."""

    username = StringField(
        "Admin Username",
        validators=[
            DataRequired(message="Please enter admin username.")
        ],
        render_kw={
            "placeholder": "Enter admin username",
            "autocomplete": "username",
        },
    )

    password = PasswordField(
        "Admin Password",
        validators=[
            DataRequired(message="Please enter admin password.")
        ],
        render_kw={
            "placeholder": "Enter admin password",
            "autocomplete": "current-password",
        },
    )

    submit = SubmitField("Login to Dashboard")


class ChangeUsernameForm(FlaskForm):
    """Form for store owner to change admin username."""

    new_username = StringField(
        "New Username",
        validators=[
            DataRequired(message="Please enter a new username."),
            Length(
                min=3,
                max=80,
                message="Username must be between 3 and 80 characters.",
            ),
        ],
        render_kw={"placeholder": "Enter new username"},
    )

    current_password = PasswordField(
        "Confirm with Current Password",
        validators=[
            DataRequired(message="Please enter current password to verify.")
        ],
        render_kw={"placeholder": "Enter current password"},
    )

    submit = SubmitField("Update Username")


class ChangePasswordForm(FlaskForm):
    """Form for store owner to change admin password."""

    current_password = PasswordField(
        "Current Password",
        validators=[
            DataRequired(message="Please enter your current password.")
        ],
        render_kw={"placeholder": "Enter current password"},
    )

    new_password = PasswordField(
        "New Password",
        validators=[
            DataRequired(message="Please enter a new password."),
            Length(
                min=6,
                message="New password must be at least 6 characters long.",
            ),
        ],
        render_kw={"placeholder": "Enter new password"},
    )

    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[
            DataRequired(message="Please confirm your new password."),
            EqualTo("new_password", message="Passwords must match."),
        ],
        render_kw={"placeholder": "Confirm new password"},
    )

    submit = SubmitField("Update Password")