"""Public website routes."""

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
from app.forms import EnquiryForm
from app.services.enquiry_service import (
    EnquiryService,
    EnquiryServiceError,
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


@main_bp.get("/db-check")
def db_check():
    """Diagnostic route to test live database connection and operations."""
    try:
        from app.models import Enquiry
        count = Enquiry.query.count()
        
        # Try a test write
        test = Enquiry(
            name="Test Connection",
            phone="1234567890",
            email="test@example.com",
            service="Laptop Repair",
            message="Test database connection",
            source_page="/db-check"
        )
        db.session.add(test)
        db.session.commit()
        
        # Clean up
        db.session.delete(test)
        db.session.commit()
        
        return {
            "status": "success",
            "message": "Database is connected and writeable.",
            "count": count
        }
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }