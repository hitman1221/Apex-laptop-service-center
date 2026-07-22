"""Store owner authentication utilities and decorator."""

from functools import wraps
from typing import Callable, Any

from flask import flash, redirect, session, url_for

from app import db
from app.models import AdminUser


def admin_required(f: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to require store owner login for administrative routes."""

    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        if not session.get("is_admin") or not session.get("admin_id"):
            flash(
                "Access restricted. Please log in as store owner to continue.",
                "warning",
            )
            return redirect(url_for("main.admin_login"))
        return f(*args, **kwargs)

    return decorated_function


def get_current_admin() -> AdminUser | None:
    """Retrieve the currently logged-in admin user object."""
    admin_id = session.get("admin_id")
    if not admin_id:
        return None
    return db.session.get(AdminUser, admin_id)


def verify_admin_user(username: str, password: str) -> AdminUser | None:
    """Check credentials against AdminUser table."""
    user = (
        db.session.query(AdminUser)
        .filter_by(username=username.strip())
        .first()
    )
    if user and user.check_password(password.strip()):
        return user
    return None


def login_admin(user: AdminUser) -> None:
    """Set admin login session variables."""
    session.clear()
    session["is_admin"] = True
    session["admin_id"] = user.id
    session["admin_username"] = user.username


def logout_admin() -> None:
    """Clear admin login session."""
    session.clear()
