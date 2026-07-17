"""Database models."""

from datetime import datetime, timezone

from app import db


class Enquiry(db.Model):
    """Customer service enquiry submitted through the website."""

    __tablename__ = "enquiries"

    id = db.Column(db.Integer, primary_key=True)

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
    pincode = db.Column(
        db.String(10),
        nullable=False,
    )
    service = db.Column(
        db.String(120),
        nullable=True,
    )
    message = db.Column(
        db.Text,
        nullable=True,
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
            f"name={self.name!r} status={self.status!r}>"
        )