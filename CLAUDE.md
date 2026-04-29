# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Stack Overview

Full-stack interview sandbox (cafe study data collection tool) with:
- **Frontend**: Vue 3 + Vite + Tailwind CSS v4 (via `@tailwindcss/vite` plugin), served on port 5173
- **Backend**: Django 4.2 + Django REST Framework, served on port 8000
- **Database**: PostgreSQL 16 (`interview_db`, user `devuser`, password `devpassword`, host `db`)
- **Environment**: Dev Container (Docker Compose) — the `db` service hostname resolves inside the container

## Running the App

**Terminal 1 — Backend:**
```bash
cd backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

## Key Architecture Notes

- Vite proxies `/api/*` requests to `http://127.0.0.1:8000`, so frontend API calls should use `/api/` paths and Django URLs should be registered under `api/` in `core/urls.py`.
- CORS is open (`CORS_ALLOW_ALL_ORIGINS = True`) for local development.
- Tailwind is integrated via the Vite plugin (`@tailwindcss/vite`), not PostCSS — no `tailwind.config.js` is needed.
- The `@` alias in Vite resolves to `frontend/src/`.
- The router uses HTML5 history mode (`createWebHistory()`).
- `axios` is available in the frontend — use it for API calls.

## Existing Auth API

The `core` app provides token-based auth (DRF `TokenAuthentication`). These endpoints are already wired up:

| Method | Path | Auth required |
|--------|------|---------------|
| POST | `/api/auth/login/` | No |
| GET | `/api/auth/me/` | Yes |
| POST | `/api/auth/logout/` | Yes |

Login returns `{ token, user }`. Send the token as `Authorization: Token <token>` on subsequent requests.

New features should go in new Django apps, not in `core`.

## Django Commands

```bash
cd backend && source venv/bin/activate

# After changing models
python manage.py makemigrations
python manage.py migrate

# Create a new app
python manage.py startapp <appname>

# Create an admin/superuser
python manage.py createsuperuser

# Django shell
python manage.py shell
```

New Django apps must be added to `INSTALLED_APPS` in `backend/core/settings.py` and their URLs included in `backend/core/urls.py` via `include()`. The Django admin is at http://localhost:8000/admin.
