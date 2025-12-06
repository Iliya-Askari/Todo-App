# Todo App (Django + DRF)

A Django + Django REST Framework todo service with a simple web UI, email-based authentication (token and JWT), a cached Mashhad weather endpoint, and Celery workers for housekeeping tasks. The project can run locally or with Docker Compose alongside Redis, smtp4dev, and Locust.

## Features
- Task model with per-user ownership, completion flag, and automatic created/updated timestamps.
- DRF viewset for tasks with completion filtering, creation-date ordering, and configurable page size (default 2, max 10).
- Email-first authentication: registration, activation via email, password change, password reset, DRF token and JWT issuance.
- Auto-generated API docs at `/swagger/`, `/redoc/`, and `/api-docs/`.
- Mashhad weather endpoint cached for 20 minutes to limit OpenWeatherMap calls.
- Celery worker and beat schedule that delete the oldest task every 10 minutes using Redis as broker/cache.
- Docker Compose stack for Django, Redis, Celery worker/beat, smtp4dev, and Locust load testing.

## Requirements (local)
- Python 3.8+
- pip and virtualenv
- Redis running at `redis://localhost:6379` if you want Celery/cache locally (optional)

## Local setup
1. **Clone and install dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Environment variables** (example `.env`)
   ```env
   SECRET_KEY=your-secret
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   # Production DB (used when DEBUG=False)
   DB_NAME=todo_db
   DB_USER=todo_user
   DB_PASSWORD=strong-password
   DB_HOST=db
   DB_PORT=5432
   ```
   - With `DEBUG=True` the app uses SQLite. When `DEBUG=False`, PostgreSQL settings above are applied.

3. **Database migrations**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser  # optional for admin access
   ```

4. **Run the server**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

5. **Access points**
   - Web UI: http://localhost:8000/
   - API docs: http://localhost:8000/swagger/ (or `/redoc/`, `/api-docs/`)
   - Admin panel: http://localhost:8000/admin/

### Celery & Redis (local)
- Broker/cache URL: `redis://redis:6379/1` (beat uses Redis cache at db 2). Override in env if needed.
- Start workers after Redis is available:
  ```bash
  celery -A core worker -l INFO
  celery -A core beat -l INFO
  ```
- Scheduled job: deletes the oldest task every 600 seconds.

## Docker Compose
1. Make sure Docker and Docker Compose are installed.
2. Launch the stack (Django, Redis, Celery worker/beat, smtp4dev, Locust):
   ```bash
   docker-compose up --build
   ```
3. Exposed services:
   - App & API: http://localhost:8000
   - smtp4dev (activation emails): http://localhost:5000
   - Locust UI: http://localhost:8089
4. Stop everything with `docker-compose down`.

## API overview
### Accounts (`/accounts/api/v1/`)
- `POST /registrations/` – register with email + password.
- `POST /token/create/` and `POST /token/discard/` – DRF token issuance and revocation.
- `POST /jwt/create/`, `/jwt/refresh/`, `/jwt/verify/` – JWT authentication.
- `PUT /changepassword/` – change password (authenticated).
- `GET /activations/confirm/<token>` and `POST /activations/resend/` – email activation flow.
- `POST /api/password_reset/` – password reset via email.

### Tasks (`/api/v1/`)
- `TaskViewSet` CRUD at `/api/v1/Tasklist/` with filtering by `complete`, ordering by `created_date`, and adjustable pagination via `?page_size=`.

### Weather
- `GET /api/v1/weather/mashhad/` – current weather for Mashhad (20-minute cache).

## Tests
Run either test suite after dependencies are installed:
```bash
pytest
# or
python manage.py test
```

## Troubleshooting
- **Dependencies fail to install**: set up internet access or configure a PyPI mirror.
- **Database connection errors**: keep `DEBUG=True` for SQLite or provide PostgreSQL variables when `DEBUG=False`.
- **Activation emails missing**: ensure smtp4dev is running (Docker) or configure SMTP settings in the environment.
