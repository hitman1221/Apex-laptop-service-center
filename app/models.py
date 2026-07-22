"""Database models."""

from datetime import datetime, timezone
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class Enquiry(db.Model):
    """Customer service enquiry submitted through the website."""

    __tablename__ = "enquiries"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.String(100),
        nullable=False,
    )

    phone = db.Column(
        db.String(20),
        nullable=False,
        index=True,
    )

    email = db.Column(
        db.String(255),
        nullable=True,
        index=True,
    )

    service = db.Column(
        db.String(120),
        nullable=False,
    )

    message = db.Column(
        db.Text,
        nullable=False,
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="new",
        index=True,
    )

    source_page = db.Column(
        db.String(255),
        nullable=False,
        default="/",
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return (
            f"<Enquiry id={self.id} "
            f"name={self.name!r} "
            f"status={self.status!r}>"
        )


class AdminUser(db.Model):
    """Store owner administrative account model."""

    __tablename__ = "admin_users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def set_password(self, password: str) -> None:
        """Hash and set the user password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if password matches stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<AdminUser id={self.id} username={self.username!r}>"