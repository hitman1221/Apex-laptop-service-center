# 💻 Apex Laptop Service Center

<p align="center">
  <strong>A professional laptop repair and service enquiry website built with Flask, PostgreSQL, Bootstrap, and automated email notifications.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.1.1-000000?logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Bootstrap-5-7952B3?logo=bootstrap&logoColor=white" alt="Bootstrap">
  <img src="https://img.shields.io/badge/Status-Production%20Ready-success" alt="Status">
</p>

---

## 📌 Project Overview

**Apex Laptop Service Center** is a responsive business website designed to help customers explore laptop repair services and submit service enquiries online.

The application validates customer details, stores every enquiry in PostgreSQL, sends an admin notification email, and optionally sends an automatic confirmation email to the customer.

### Business Information

- **Business:** Apex Laptop Service Center
- **Rating:** 4.7 / 5
- **Experience:** 10 Years in Business
- **Location:** Kandivali East, Mumbai
- **Working Hours:** Daily, 9:00 AM – 8:00 PM
- **Phone:** 08460450742
- **WhatsApp:** +91 70211 61621
- **Email:** apexlaptopsolution@gmail.com

---

## ✨ Key Features

- Modern and responsive business website
- Laptop repair service showcase
- Customer enquiry and callback form
- Optional customer email field
- Indian mobile number validation
- Server-side validation using WTForms
- CSRF protection
- PostgreSQL database storage
- SQLAlchemy ORM
- Flask database migrations
- Admin enquiry notification email
- Customer confirmation email
- Professional HTML email templates
- Thank-you confirmation page
- Production health-check endpoint
- Environment-based configuration
- Clean service-layer architecture
- Gunicorn production server support

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Backend | Python, Flask |
| Database | PostgreSQL |
| ORM | Flask-SQLAlchemy |
| Forms & Validation | Flask-WTF, WTForms |
| Migrations | Flask-Migrate |
| Email Service | Flask-Mail, Brevo SMTP |
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Production Server | Gunicorn |
| Configuration | python-dotenv |

---

## 🏗️ Project Architecture

```text
apex-laptop-service-center/
│
├── app/
│   ├── content/
│   │   └── Website content and service data
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── email_service.py
│   │   └── enquiry_service.py
│   │
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   ├── templates/
│   │   ├── emails/
│   │   │   ├── admin_enquiry.html
│   │   │   └── customer_confirmation.html
│   │   ├── errors/
│   │   │   └── 500.html
│   │   ├── index.html
│   │   └── thank-you.html
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── validators.py
│   │
│   ├── __init__.py
│   ├── forms.py
│   ├── models.py
│   └── routes.py
│
├── migrations/
├── config.py
├── run.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🔄 Application Workflow

```text
Customer submits enquiry
          ↓
WTForms validation
          ↓
Enquiry saved in PostgreSQL
          ↓
Admin notification email
          ↓
Customer email provided?
      ┌───┴───┐
     Yes      No
      ↓        ↓
Confirmation  Skip
email sent
          ↓
Thank-you page
```

---

## 🗃️ Enquiry Data

Each enquiry stores the following information:

| Field | Required |
|---|---|
| Full Name | Yes |
| Mobile Number | Yes |
| Email Address | No |
| Required Service | Yes |
| Issue Description | Yes |
| Source Page | Automatically recorded |
| Created At | Automatically recorded |

---

## 🔗 Available Routes

| Method | Endpoint | Description |
|---|---|---|
| GET, POST | `/` | Homepage and enquiry submission |
| GET | `/thank-you` | Successful enquiry confirmation page |
| GET | `/health` | Application health-check endpoint |

Example health response:

```json
{
  "status": "healthy",
  "service": "Apex Laptop Service Center"
}
```

---

## ⚙️ Local Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd apex-laptop-service-center
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

Create a `.env` file in the project root.

```env
FLASK_ENV=development
SECRET_KEY=replace_with_a_secure_secret_key

DATABASE_URL=postgresql://postgres:your_password@localhost/apex_service_db

MAIL_SERVER=smtp-relay.brevo.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false

MAIL_USERNAME=your_brevo_smtp_username
MAIL_PASSWORD=your_brevo_smtp_key

MAIL_DEFAULT_SENDER_NAME=Apex Laptop Service Center
MAIL_DEFAULT_SENDER_EMAIL=your_verified_sender@example.com

ENQUIRY_RECIPIENT_EMAIL=apexlaptopsolution@gmail.com
SEND_CUSTOMER_CONFIRMATION_EMAIL=true
```

> Never commit your real `.env`, SMTP password, database password, or secret key to GitHub.

---

## 🗄️ Database Setup

Create the PostgreSQL database first, then run migrations:

```bash
flask db upgrade
```

To create a new migration after changing models:

```bash
flask db migrate -m "Describe your changes"
flask db upgrade
```

---

## ▶️ Run the Application

```bash
python run.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 🚀 Production Deployment

Run the project with Gunicorn:

```bash
gunicorn run:app
```

For cloud deployment, configure all environment variables in the hosting dashboard instead of uploading the `.env` file.

### Recommended production configuration

- PostgreSQL production database
- Verified business sender email
- Custom business domain
- SPF, DKIM, and DMARC records
- HTTPS enabled
- Secure secret key
- Debug mode disabled

---

## 📧 Email Notification Flow

### Admin Notification

After a successful enquiry, the business receives:

- Customer name
- Phone number
- Email address
- Selected service
- Customer message

### Customer Confirmation

When the customer provides an email address, the system sends a confirmation containing:

- Customer name
- Selected service
- Confirmation that the enquiry was received
- Expected follow-up message

Email failures do not remove or roll back the saved enquiry.

---

## 🛡️ Security

- CSRF protection using Flask-WTF
- Server-side input validation
- ORM-based database operations
- Environment-based credentials
- Optional email validation
- Indian phone number validation
- Production error handling
- Sensitive data excluded through `.gitignore`

---

## 📸 Screenshots

Create a `screenshots` folder and add project images using these names:

```text
screenshots/
├── homepage.png
├── services.png
├── enquiry-form.png
├── thank-you-page.png
└── admin-email.png
```

Then uncomment the image blocks below.

<!--
### Homepage

![Homepage](screenshots/homepage.png)

### Services

![Services](screenshots/services.png)

### Enquiry Form

![Enquiry Form](screenshots/enquiry-form.png)

### Thank-You Page

![Thank-You Page](screenshots/thank-you-page.png)

### Admin Email Notification

![Admin Email](screenshots/admin-email.png)
-->

---

## 🧪 Testing Checklist

Before deployment, verify:

- [ ] Homepage loads successfully
- [ ] Required form fields show validation errors
- [ ] Optional email can remain empty
- [ ] Invalid email is rejected
- [ ] Invalid phone number is rejected
- [ ] Enquiry is stored in PostgreSQL
- [ ] Admin email is triggered
- [ ] Customer confirmation email is triggered
- [ ] Thank-you page opens after submission
- [ ] `/health` returns a successful response
- [ ] `.env` is not committed
- [ ] Debug mode is disabled in production

---

## 🔮 Future Improvements

- Admin login and enquiry dashboard
- Enquiry status management
- Search and filter enquiries
- CSV and Excel export
- WhatsApp notification integration
- Appointment scheduling
- Background email queue
- Automated email retry system
- Service pricing management
- Customer feedback and review system
- Analytics dashboard

---

## 📦 Main Dependencies

```text
Flask==3.1.1
Flask-Migrate==4.1.0
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.2
WTForms==3.2.1
email-validator==2.2.0
psycopg2-binary==2.9.10
python-dotenv==1.1.0
gunicorn==23.0.0
Flask-Mail==0.10.0
```

---

## 👨‍💻 Developer

**Abusufiyan**

Python Backend Developer focused on Flask, Django, PostgreSQL, REST APIs, and production-ready web applications.

- GitHub: [abusufiyan7518](https://github.com/abusufiyan7518)
- Email: apexlaptopsolution@gmail.com

---

## 📄 License

This project was developed for **Apex Laptop Service Center**.

The business name, contact details, branding, and website content belong to the respective business owner. The source code may not be reused commercially without permission.

---

<p align="center">
  Built with ❤️ using Python, Flask, PostgreSQL, and Bootstrap.
</p>
