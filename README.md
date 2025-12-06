# Todo App (Django + DRF)

A Django + Django REST Framework Todo service that includes a web UI, authentication APIs (Token & JWT), a weather endpoint, and Celery workers for background tasks. The stack is ready for local development or Docker-based deployment and ships with Swagger/Redoc auto-generated docs.

## Features
- **Task model with user ownership** and completion flag with automatic created/updated timestamps.【F:core/todo/models.py†L9-L17】
- **Task management API** with completion filtering, creation-date ordering, and custom pagination configurable via `page_size`.【F:core/todo/api/v1/views.py†L11-L22】【F:core/todo/api/v1/pagination.py†L4-L11】
- **Email-based auth & registration**, DRF token and JWT issuance, password change, and account activation via email.【F:core/accounts/models.py†L12-L83】【F:core/accounts/api/v1/urls.py†L6-L48】
- **API documentation** available at `/swagger/`, `/redoc/`, and `/api-docs/`.【F:core/core/urls.py†L18-L66】
- **Mashhad weather service** with a 20-minute cache to avoid repeated OpenWeatherMap requests.【F:core/todo/api/v1/wather/views.py†L5-L22】
- **Celery worker and beat scheduler** that remove the oldest task every 10 minutes, using Redis as broker/cache.【F:core/core/settings.py†L198-L216】【F:core/todo/tasks.py†L4-L13】
- Ready-to-run **Docker Compose** stack including Redis, Celery worker/beat, smtp4dev for activation emails, and Locust for load testing.【F:docker-compose.yml†L1-L57】

## Prerequisites (local run)
- Python 3.8+
- (Optional) Redis for cache/Celery
- pip and virtualenv

## Quickstart (local)
1. Clone the repo and move to the project root.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   > If PyPI access is restricted, configure your proxy or mirror first.
4. Configure environment variables (sample `.env`):
   ```env
   SECRET_KEY=your-secret
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   # Production database (used when DEBUG=False)
   DB_NAME=todo_db
   DB_USER=todo_user
   DB_PASSWORD=strong-password
   DB_HOST=db
   DB_PORT=5432
   ```
   - With `DEBUG=True` SQLite is used by default; when `DEBUG=False` the above PostgreSQL settings are applied.【F:core/core/settings.py†L102-L123】
5. Prepare the database:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser  # optional for admin login
   ```
6. Run the development server:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
7. Access points:
   - Web UI: `http://localhost:8000/`
   - API docs: `http://localhost:8000/swagger/` or `http://localhost:8000/redoc/`
   - Admin panel: `http://localhost:8000/admin/`

## Celery & Redis
- Broker/cache URL is set to `redis://redis:6379`.【F:core/core/settings.py†L198-L215】
- For a local run without Docker, ensure Redis is available on port 6379, then start workers:
  ```bash
  celery -A core worker -l INFO
  celery -A core beat -l INFO
  ```
- The scheduled `delete_task` job removes the oldest task every 600 seconds.【F:core/core/settings.py†L202-L206】【F:core/todo/tasks.py†L4-L13】

## Running with Docker Compose
1. Ensure Docker and Docker Compose are installed.
2. Start all services (Django, Redis, Celery worker/beat, smtp4dev, and Locust):
   ```bash
   docker-compose up --build
   ```
3. Key ports:
   - Web & API: `http://localhost:8000`
   - smtp4dev (activation emails): `http://localhost:5000`
   - Locust (load test UI): `http://localhost:8089`
4. Stop services:
   ```bash
   docker-compose down
   ```

## API Usage
### Authentication & Accounts
Base path: `/accounts/api/v1/`
- Register: `POST /registrations/` (body: email, password, password_2)
- Create DRF token: `POST /token/create/`
- Discard DRF token: `POST /token/discard/`
- Create JWT: `POST /jwt/create/` with refresh/verify at `/jwt/refresh/` and `/jwt/verify/`
- Change password: `PUT /changepassword/`
- Activate account: `GET /activations/confirm/<token>` and resend via `POST /activations/resend/`
- Password reset: `POST /api/password_reset/`
【F:core/accounts/api/v1/urls.py†L6-L48】

### Tasks
Base path: `/api/v1/`
- CRUD is handled by the `Tasklist` viewset (authentication required).
- Filter by `complete` and order by `created_date` using standard DRF query params.
- Default pagination: 2 items per page, adjustable via `?page_size=...` up to a max of 10.【F:core/todo/api/v1/views.py†L11-L22】【F:core/todo/api/v1/pagination.py†L4-L11】
- Example routes:
  - `GET /api/v1/Tasklist/`
  - `POST /api/v1/Tasklist/` (only a title is required; user is set automatically)
  - `GET /api/v1/Tasklist/<id>/`
  - `PATCH /api/v1/Tasklist/<id>/` (edit title or completion status)
  - `DELETE /api/v1/Tasklist/<id>/`

### Weather
- `GET /api/v1/weather/mashhad/` returns city, country, temperature, and description. Response is cached for 20 minutes.【F:core/todo/api/v1/wather/views.py†L5-L22】

## Additional Notes
- Swagger/Redoc and `api-docs` are enabled via `drf_yasg` and DRF configuration.【F:core/core/urls.py†L18-L66】
- The custom user model uses email for login; in production ensure `is_verified` is managed appropriately when creating users.【F:core/accounts/models.py†L12-L83】
- The Dockerfile uses `python:3.8-slim-buster` and installs dependencies before copying source—follow the same steps for manual builds.【F:Dockerfile†L1-L16】
- For load testing, see `core/locust/locustfile.py`; master/worker services are defined in `docker-compose.yml`.【F:docker-compose.yml†L41-L53】

## Tests
- After installing dependencies, run:
  ```bash
  pytest
  ```
  or
  ```bash
  python manage.py test
  ```

## Quick Troubleshooting
- **Dependencies do not install**: configure internet access or a PyPI mirror/proxy.
- **Database errors**: for production, set PostgreSQL vars (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`) or keep `DEBUG=True` for SQLite.
- **No activation email received**: in development, run smtp4dev via Docker or update SMTP settings in the environment variables.【F:core/core/settings.py†L188-L194】【F:docker-compose.yml†L29-L40】
