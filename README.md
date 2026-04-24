# Engineering Interview — Expense Management Module

Welcome. You have **60 minutes** to build an expense management module on top of this full-stack sandbox. You are free to use any external resources, documentation, or AI tools throughout the exercise.

---

## The Exercise

Build a module that allows employees to submit expenses for manager review and approval.

### User Roles

| Role | Description |
|------|-------------|
| **Submitter** | A regular employee who creates and manages their own expense requests |
| **Manager** | Reviews all submitted expenses and approves or rejects them |

### Required Features

**Submitter view**
- View a list of their own submitted expenses and their current status
- Create a new expense (amount, category, description, date, receipt/supporting details)
- Edit an expense that has not yet been approved or rejected

**Manager view**
- View all submitted expenses across all users
- Approve an expense
- Reject an expense with a required rejection reason

---

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3 + Vite + Tailwind CSS v4 |
| Backend | Django 4.2 + Django REST Framework |
| Database | PostgreSQL 16 |

---

## Getting Started

Open a split terminal and run both servers simultaneously.

**Terminal 1 — Backend**
```bash
cd backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

**Terminal 2 — Frontend**
```bash
cd frontend
npm run dev
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

---

## Architecture Notes

- Vite proxies `/api/*` → `http://127.0.0.1:8000`, so all frontend API calls should use `/api/` paths. Register Django URLs under `api/` in `backend/core/urls.py`.
- CORS is fully open (`CORS_ALLOW_ALL_ORIGINS = True`) — no CORS configuration needed.
- Tailwind is loaded via the Vite plugin (`@tailwindcss/vite`). There is no `tailwind.config.js` — utility classes work out of the box.
- The `@` alias in Vite resolves to `frontend/src/`.

### Creating a new Django app

```bash
cd backend && source venv/bin/activate
python manage.py startapp <appname>
```

Then:
1. Add `'<appname>'` to `INSTALLED_APPS` in `backend/core/settings.py`
2. Include its URLs in `backend/core/urls.py`
3. Run `python manage.py makemigrations && python manage.py migrate`

### Useful Django commands

```bash
cd backend && source venv/bin/activate

python manage.py makemigrations   # generate migrations after model changes
python manage.py migrate          # apply migrations
python manage.py seed_users       # create the two sample users (see below)
python manage.py createsuperuser  # create an admin user
python manage.py shell            # interactive Django shell
```

The Django admin is available at http://localhost:8000/admin — useful for quickly creating test users and inspecting data.

### Sample users

Run `python manage.py seed_users` after migrating to create:

| Name | Username | Password | Role |
|------|----------|----------|------|
| Sample Submitter | `submitter` | `password123` | Regular user |
| Sample Manager | `manager` | `password123` | Staff user (`is_staff=True`) |

The command is idempotent — safe to run multiple times.

---

## Suggested Approach

This is intentionally open-ended. A reasonable path through the problem:

1. **Model** — Define an `Expense` model with fields for amount, category, description, date, status (`pending` / `approved` / `rejected`), submitter (FK to User), and rejection reason.
2. **API** — Create DRF serializers and views (or viewsets) for CRUD on expenses, plus approve/reject actions. Use Django's built-in `User` model for authentication.
3. **Frontend** — Build two Vue views: one for the submitter dashboard and one for the manager dashboard. Wire them to the API with `fetch` or `axios`.
4. **Auth** — Django session auth or token auth (DRF ships `TokenAuthentication`) both work fine for this exercise.

You do not need to implement user registration — creating users via the Django admin or fixtures is perfectly acceptable.

---

## Evaluation Criteria

- Does the core workflow function end-to-end (create → submit → approve/reject)?
- Is the data model reasonable and the API well-structured?
- Is the UI clear and usable?
- Is the code organized and readable?
