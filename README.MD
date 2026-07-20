# Apex Laptop Service Center

A professional Flask-based website for **Apex Laptop Service Center** with an enquiry management system, PostgreSQL database integration, and automated email notifications.

## Features

- Responsive Bootstrap-based website
- Service enquiry form
- Server-side validation with WTForms
- PostgreSQL database integration
- SQLAlchemy ORM
- Flask-Migrate database migrations
- Admin enquiry notification emails
- Customer confirmation emails
- CSRF protection
- Health check endpoint
- Clean service-layer architecture
- Production-ready configuration using environment variables

---

## Tech Stack

- Python 3
- Flask
- PostgreSQL
- SQLAlchemy
- Flask-Mail
- Flask-WTF
- Bootstrap 5
- Gunicorn

---

## Project Structure

```text
app/
├── content/
├── forms.py
├── models.py
├── routes.py
├── services/
│   ├── email_service.py
│   └── enquiry_service.py
├── static/
├── templates/
│   ├── emails/
│   ├── errors/
│   ├── index.html
│   └── thank-you.html
├── utils/
└── __init__.py

config.py
run.py
requirements.txt
```

---

## Installation

```bash
git clone <repository-url>
cd apex-laptop-service-center

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

```env
SECRET_KEY=your_secret_key

DATABASE_URL=postgresql://username:password@localhost/database_name

MAIL_SERVER=smtp-relay.brevo.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_brevo_username
MAIL_PASSWORD=your_brevo_password

MAIL_DEFAULT_SENDER_NAME=Apex Laptop Service Center
MAIL_DEFAULT_SENDER_EMAIL=your_verified_sender@example.com

ENQUIRY_RECIPIENT_EMAIL=your_business_email@example.com

SEND_CUSTOMER_CONFIRMATION_EMAIL=true
```

---

## Database

```bash
flask db upgrade
```

---

## Run the Application

```bash
python run.py
```

or

```bash
flask run
```

---

## Production

```bash
gunicorn run:app
```

---

## Email Workflow

1. Customer submits enquiry.
2. Enquiry is validated.
3. Data is saved in PostgreSQL.
4. Admin receives notification email.
5. Customer receives confirmation email (if email provided).

---

## Security

- CSRF Protection
- Server-side validation
- Environment-based configuration
- SQLAlchemy ORM
- Secure SMTP authentication

---

## License

This project was developed for Apex Laptop Service Center.
