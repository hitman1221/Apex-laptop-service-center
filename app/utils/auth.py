"""Store owner authentication utilities and decorator."""

from functools import wraps
from typing import Callable, Any

from flask import current_app, flash, redirect, session, url_for


def admin_required(f: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to require store owner login for administrative routes."""

    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        if not session.get("is_admin"):
            flash(
                "Access restricted. Please log in as store owner to continue.",
                "warning",
            )
            return redirect(url_for("main.admin_login"))
        return f(*args, **kwargs)

    return decorated_function


def verify_admin_credentials(username: str, password: str) -> bool:
    """Check if provided credentials match configured admin credentials."""
    expected_username = current_app.config.get("ADMIN_USERNAME", "admin")
    expected_password = current_app.config.get("ADMIN_PASSWORD", "apex@123")

    return username.strip() == expected_username and password == expected_password


def login_admin(username: str) -> None:
    """Set admin login session flags."""
    session.clear()
    session["is_admin"] = True
    session["admin_username"] = username


def logout_admin() -> None:
    """Clear admin login session."""
    session.pop("is_admin", None)
    session.pop("admin_username", None)
