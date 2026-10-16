# SocietySync

Apartment maintenance tracker and notice board built with Django. Residents raise maintenance tickets and follow their progress; administrators manage them from an enhanced Django Admin and notify residents by email.

## Features

**Residents**
- Register, log in, and raise tickets by category (Plumbing, Electrical, Security, Other) with an optional photo
- Track each ticket's status history, including timestamps and admin notes
- Read society notices, with urgent ones pinned to the top

**Administrators**
- Staff users are redirected to the admin dashboard on login; residents go to their portal
- Dashboard with live counts of Open, In Progress, Resolved, and Overdue tickets
- Overdue detection for unresolved tickets older than a configurable threshold (default: 3 days)
- Email notifications:
  - Status-change emails to the resident, including the admin's note
  - Urgent notices broadcast to all registered residents
  - Email failures are caught and logged, so they never block a database save
- `check_overdue` management command that emails admins a summary of overdue tickets (suitable for cron)

**File upload validation**
- Allowed types: `.jpg`, `.jpeg`, `.png`, `.webp`
- Maximum size: 5 MB
- Checked on both the client and the server

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6.x, Python 3.11+ |
| Database | SQLite (default), PostgreSQL-ready |
| Frontend | Django templates, [Pico.css](https://picocss.com/) via CDN |
| Images | Pillow |
| Config | python-dotenv |
| Email | Django email backend (console or SMTP) |

## Project Structure

```text
Society-Maintenance-Tracker/
├── manage.py
├── society_sync/            # Project settings, URLs, WSGI
├── complaints/              # Main app
│   ├── models.py            # Complaint, StatusHistory, Notice
│   ├── forms.py             # Ticket form and upload validation
│   ├── views.py             # Resident views
│   ├── admin.py             # Admin dashboard and workflow
│   ├── services.py          # Email notifications
│   └── management/commands/
│       └── check_overdue.py
├── templates/               # Base, dashboard, ticket, auth, admin templates
└── static/
```

## Getting Started

### 1. Clone and enter the project

```bash
git clone https://github.com/your-username/Society-Maintenance-Tracker.git
cd Society-Maintenance-Tracker
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install django pillow python-dotenv
```

### 4. Configure environment variables

Create a `.env` file next to `manage.py`:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DJANGO_EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Emails are printed to the terminal with the console backend, which is fine for development. To send real emails, see [Email Configuration](#email-configuration).

### 5. Migrate and create an admin user

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run the server

```bash
python manage.py runserver
```

- Resident portal: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## Email Configuration

To use SMTP (for example Gmail with an App Password), update `.env`:

```env
DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL="SocietySync <your-email@gmail.com>"
```

## Usage

### Ticket lifecycle

1. A resident raises a ticket with a category and optional photo.
2. An admin updates its status and adds an optional note in the admin panel.
3. Each status change is saved to the ticket's history and emailed to the resident.

### Checking for overdue tickets

```bash
# Tickets unresolved for more than 3 days (default)
python manage.py check_overdue

# Custom threshold
python manage.py check_overdue --days 0
```

To run it daily, add a cron entry such as:

```cron
0 9 * * * cd /path/to/Society-Maintenance-Tracker && venv/bin/python manage.py check_overdue
```

## Production Notes

- Set `DEBUG=False` and use a strong, unique `SECRET_KEY`
- Never commit `.env` (add it to `.gitignore`)
- Use PostgreSQL and a real SMTP provider
- Serve uploaded media and static files through your web server