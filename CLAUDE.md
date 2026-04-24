# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Stack Overview

Full-stack interview sandbox with:
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

## Django Commands

```bash
cd backend && source venv/bin/activate

# Apply migrations
python manage.py migrate

# Create a new app
python manage.py startapp <appname>

# Django shell
python manage.py shell
```

New Django apps must be added to `INSTALLED_APPS` in `backend/core/settings.py` and their URLs included in `backend/core/urls.py`.
