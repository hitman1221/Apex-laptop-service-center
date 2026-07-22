"""Public website routes."""

# pyrefly: ignore [missing-import]
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from app.content import (
    BRANDS,
    BUSINESS_HIGHLIGHTS,
    FAQS,
    OTHER_BRANDS,
    PROCESS_STEPS,
    REPAIR_PROCESS,
    SERVICES,
    TESTIMONIALS,
    WHY_CHOOSE_US,
)
from app.forms import (
    AdminLoginForm,
    ChangePasswordForm,
    ChangeUsernameForm,
    EnquiryForm,
)
from app.services.enquiry_service import (
    EnquiryService,
    EnquiryServiceError,
)
from app.utils.auth import (
    admin_required,
    get_current_admin,
    login_admin,
    logout_admin,
    verify_admin_user,
)
from app import db


main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def home():
    """Render homepage and process enquiry submissions."""

    form = EnquiryForm()

    if form.validate_on_submit():
        try:
            EnquiryService.create_enquiry(
                name=form.name.data.strip(),
                phone=form.phone.data.strip(),
                email=(
                    form.email.data.strip()
                    if form.email.data
                    else None
                ),
                service=form.service.data,
                message=form.message.data.strip(),
                source_page=request.path,
            )

        except EnquiryServiceError:
            current_app.logger.exception(
                "Unable to create customer enquiry."
            )

            flash(
                (
                    "We could not submit your enquiry "
                    "right now. Please try again or "
                    "contact the service center directly."
                ),
                "danger",
            )

        else:
            return redirect(
                url_for("main.thank_you")
            )

    elif request.method == "POST":
        current_app.logger.warning(
            "Enquiry form validation failed: %s",
            form.errors,
        )

        flash(
            (
                "Some details are missing or invalid. "
                "Please check the highlighted fields."
            ),
            "danger",
        )

    return render_template(
        "index.html",
        form=form,
        services=SERVICES,
        brands=BRANDS,
        business_highlights=BUSINESS_HIGHLIGHTS,
        process_steps=PROCESS_STEPS,
        why_choose_us=WHY_CHOOSE_US,
        repair_process=REPAIR_PROCESS,
        faqs=FAQS,
        other_brands=OTHER_BRANDS,
        testimonials=TESTIMONIALS,
    )


@main_bp.get("/thank-you")
def thank_you():
    """Render the enquiry confirmation page."""

    return render_template("thank-you.html")


@main_bp.get("/health")
def health():
    """Return a lightweight health-check response."""

    return {
        "status": "healthy",
        "service": current_app.config["BUSINESS_NAME"],
    }


@main_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Render store owner login page and process credentials."""

    form = AdminLoginForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()

        user = verify_admin_user(username, password)
        if user:
            login_admin(user)
            flash("Welcome, Store Owner! You are now logged in.", "success")
            return redirect(url_for("main.admin_enquiries"))
        else:
            flash("Invalid admin username or password.", "danger")

    return render_template("admin/login.html", form=form)


@main_bp.get("/admin/logout")
def admin_logout():
    """Log out the store owner and redirect to homepage."""

    logout_admin()
    flash("You have been logged out of the admin portal.", "info")
    return redirect(url_for("main.home"))


@main_bp.get("/dashboard")
@main_bp.get("/admin/enquiries")
@admin_required
def admin_enquiries():
    """Render customer call requests and enquiry management dashboard."""

    status = request.args.get("status", "all").strip().lower()
    enquiries = EnquiryService.get_all_enquiries(status=status)
    stats = EnquiryService.get_enquiry_stats()

    return render_template(
        "admin/enquiries.html",
        enquiries=enquiries,
        stats=stats,
        current_status=status,
    )


@main_bp.post("/admin/enquiries/<int:enquiry_id>/status")
@admin_required
def update_admin_enquiry_status(enquiry_id: int):
    """Update status of a customer enquiry."""

    new_status = request.form.get("status", "").strip().lower()

    try:
        updated = EnquiryService.update_enquiry_status(
            enquiry_id, new_status
        )
        if updated:
            flash(
                f"Request #{enquiry_id} status updated to '{new_status.replace('_', ' ')}'.",
                "success",
            )
        else:
            flash(f"Enquiry #{enquiry_id} not found.", "warning")
    except EnquiryServiceError:
        flash("Failed to update status. Please try again.", "danger")

    return redirect(
        request.referrer or url_for("main.admin_enquiries")
    )


@main_bp.get("/admin/settings")
@admin_required
def admin_settings():
    """Render store owner security and credentials settings page."""

    current_admin = get_current_admin()
    username_form = ChangeUsernameForm(new_username=current_admin.username if current_admin else "")
    password_form = ChangePasswordForm()

    return render_template(
        "admin/settings.html",
        current_admin=current_admin,
        username_form=username_form,
        password_form=password_form,
    )


@main_bp.post("/admin/change-username")
@admin_required
def admin_change_username():
    """Process store owner username update."""

    current_admin = get_current_admin()
    username_form = ChangeUsernameForm()
    password_form = ChangePasswordForm()

    if username_form.validate_on_submit():
        new_user = username_form.new_username.data.strip()
        curr_pass = username_form.current_password.data.strip()

        if not current_admin.check_password(curr_pass):
            flash("Current password is incorrect. Unable to update username.", "danger")
        else:
            current_admin.username = new_user
            db.session.commit()
            login_admin(current_admin)
            flash(f"Username successfully updated to '{new_user}'.", "success")
            return redirect(url_for("main.admin_settings"))

    return render_template(
        "admin/settings.html",
        current_admin=current_admin,
        username_form=username_form,
        password_form=password_form,
    )


@main_bp.post("/admin/change-password")
@admin_required
def admin_change_password():
    """Process store owner password update."""

    current_admin = get_current_admin()
    username_form = ChangeUsernameForm(new_username=current_admin.username if current_admin else "")
    password_form = ChangePasswordForm()

    if password_form.validate_on_submit():
        curr_pass = password_form.current_password.data.strip()
        new_pass = password_form.new_password.data.strip()

        if not current_admin.check_password(curr_pass):
            flash("Current password is incorrect. Unable to update password.", "danger")
        else:
            current_admin.set_password(new_pass)
            db.session.commit()
            flash("Password successfully updated. Please use your new password next time.", "success")
            return redirect(url_for("main.admin_settings"))

    return render_template(
        "admin/settings.html",
        current_admin=current_admin,
        username_form=username_form,
        password_form=password_form,
    )


