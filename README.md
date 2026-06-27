# Personal-Finance-Webapp

A simple personal finance webapp to manage day-to-day expenses and track your
current balance. Built with Django.

## Features

- **Dashboard** showing current balance, total income, and total expense
- **Transactions**: add, edit, and delete income/expense entries
- Categorize transactions (food, transport, housing, salary, etc.)
- Clean, responsive UI (Bootstrap 5)
- Django admin for power management

## Tech stack

- Python 3.12
- Django 5.1
- SQLite (default, zero-config)

## Getting started

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply database migrations
python manage.py migrate

# 4. Create a user to sign in with (required — all pages need login)
python manage.py createsuperuser

# 5. Run the development server
python manage.py runserver
```

Then open http://127.0.0.1:8000/ and sign in with the user you created.

## Configuration

Settings are read from environment variables (see `.env.example`):

| Variable | Default | Notes |
|----------|---------|-------|
| `DJANGO_SECRET_KEY` | insecure dev key | **Set a strong value in production.** |
| `DJANGO_DEBUG` | `True` | Set to `False` in production. |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated hostnames. |

All transaction pages require authentication.

## Running tests

```bash
python manage.py test
```

## Project structure

```
finance/        Django project settings and URLs
expenses/       The expense-management app (models, views, forms, templates)
```
