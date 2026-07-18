# QueueHub

A digital queue / token booking system — customers reserve tokens online,
organizations manage the live queue from one dashboard. No receptionist role;
everything happens between **Customer** and **Organization**.

```
queuehub/
  backend/     FastAPI + PostgreSQL + JWT + WebSockets   → backend/README.md
  frontend/    React + Vite + Tailwind                    → frontend/README.md
```

## Quick start

**1. Backend**
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # set DATABASE_URL to a real Postgres instance
python -m app.seed     # optional demo data
uvicorn app.main:app --reload
```

**2. Frontend** (new terminal)
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Visit http://localhost:5173. If you ran the seed script, log in as:
- Organization: `apollo@queuehub.demo` / `password123`
- Customer: `customer@queuehub.demo` / `password123`

## What's built vs. what's next

This scaffold implements the full core loop end-to-end and has been
smoke-tested (register → create service → book token → FCFS conflict →
call/complete → walk-in → history → reports all verified against the API):

- Two-role auth (Customer / Organization) with JWT
- Domain → Organization → Service → Service detail browsing
- Token booking with **FCFS enforced at the database level** (unique
  constraint + integrity-error handling — no race-condition window)
- Live queue via WebSocket (`/ws/queue/{service_id}`), with REST polling as
  a fallback on pages that don't hold a socket open
- Organization dashboard, queue management (call next / skip / complete),
  walk-in booking into the same queue as online bookings, manage services
  (CRUD + enable/disable), and a reports view

Deliberately left as stubs or omitted, per the "Future Enhancements" section
of the spec: SMS/WhatsApp push, AI wait-time prediction, multi-branch orgs,
payments, feedback, a dedicated analytics dashboard, appointment booking, and
a native mobile app. In-app notifications (the DB-backed kind) are wired up;
the milestone triggers (5/3/1 remaining) are a good next addition on top of
the existing `Notification` model and WebSocket broadcast.

Also worth doing before production: switch `Base.metadata.create_all` to
Alembic migrations (already in `requirements.txt`), and move the DB calls in
async route handlers to a threadpool or an async SQLAlchemy engine so they
don't block the event loop under load.
