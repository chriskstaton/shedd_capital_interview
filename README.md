## notes
 
Build a frontend component of a custom form that includes the following subcomponents, builds a JSON object with the following fields 

 Customer Name (string): [text input field]

 occupation (string): professional/student/unemployed  [use menu dropdown with options]

 ordered item (string): coffee, tea, or juice [use menu dropdown with options]

 time of the order placed (24hr HHMMSS number):

 time order received (24hr HHMMSS number):

 Customer's rating of the service on scale of 1-10 (number): [text input field]

print json object to console


# Engineering Interview — Cafe Study Data Collection Tool

Welcome. You have **60 minutes** to build a data collection tool on top of this full-stack sandbox. You are free to use any external resources, documentation, or AI tools throughout the exercise.

---

## The Exercise

A team of sociologists is conducting a study on how people experience service at a cafe. They need a custom software tool to help their researchers collect data about customers in real time.

Your role is that of a developer brought in to help design and build this tool. The researchers will be using it during active, busy periods at the cafe — so the interface must be built for **speed and accuracy**. Data entry needs to be fast, intuitive, and minimize the chance of mistakes under pressure.


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

## Suggested Approach

This is intentionally open-ended. A reasonable path through the problem:

1. **Clarify requirements** — Ask clarifying questions that should inform your model and UI design.
2. **Model** — Define a Django model that represents a single customer observation, based on the requirements you've gathered.
3. **API** — Create Django RestFramework serializers and views for creating and listing observations.
4. **Frontend** — Build a Vue interface optimized for fast, accurate data entry in a high-pressure environment.

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
python manage.py createsuperuser  # create an admin user
python manage.py shell            # interactive Django shell
```

The Django admin is available at http://localhost:8000/admin — useful for quickly inspecting and managing data.

---

