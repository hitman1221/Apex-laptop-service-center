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
    FAQ_ITEMS,
    PROCESS_STEPS,
    SERVICES,
    WHY_CHOOSE_ITEMS,
)
from app.forms import EnquiryForm
from app.services.enquiry_service import (
    EnquiryService,
    EnquiryServiceError,
)


main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def home():
    """Render the landing page and process enquiry submissions."""

    form = EnquiryForm()

    if form.validate_on_submit():
        try:
            EnquiryService.create_enquiry(
                name=form.name.data,
                phone=form.phone.data,
                email=form.email.data,
                pincode=form.pincode.data,
                service=form.service.data,
                message=form.message.data,
                source_page=request.path,
            )

        except EnquiryServiceError:
            flash(
                (
                    "We could not submit your enquiry right now. "
                    "Please try again or call the service center."
                ),
                "danger",
            )

        else:
            return redirect(url_for("main.thank_you"))

    elif request.method == "POST":
        flash(
            (
                "Please review the highlighted fields "
                "and submit the form again."
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
        why_choose_items=WHY_CHOOSE_ITEMS,
        faq_items=FAQ_ITEMS,
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