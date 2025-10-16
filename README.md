# Appointments API + Stripe (Django + DRF)

A minimal API-only Django app that demonstrates:
- `Appointment` model (`provider_name`, `appointment_time`, `client_email`)
- REST API to create/list/retrieve appointments (DRF)
- Stripe Checkout (test keys)

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # or create .env; see below
python manage.py migrate
python manage.py runserver
```