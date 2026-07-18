# QueueHub Backend (FastAPI)

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then edit DATABASE_URL / SECRET_KEY
```

Create the PostgreSQL database referenced in `DATABASE_URL` (e.g. `createdb queuehub`),
then run:

```bash
uvicorn app.main:app --reload
```

Tables are auto-created on startup via `Base.metadata.create_all`. For real
production use, switch to Alembic migrations (already in requirements.txt).

Optional: seed demo data (one organization with 4 services + one demo customer):

```bash
python -m app.seed
```

API docs: http://localhost:8000/docs

## Project layout

```
app/
  main.py            FastAPI app, CORS, router wiring
  config.py           env-based settings
  database.py          SQLAlchemy engine/session/Base
  models.py            ORM models (User, Organization, Service, Token, Booking, Notification)
  schemas.py           Pydantic request/response schemas
  security.py           password hashing + JWT
  deps.py               auth dependencies (get_current_user, require_customer, require_organization)
  queue_utils.py        shared queue math (current token, wait time, availability)
  ws_manager.py          in-memory WebSocket connection manager, per service_id
  seed.py                 optional demo data
  routers/
    auth.py               register / login
    customer.py            browse domains/orgs/services, book token (FCFS), history, notifications
    organization.py          dashboard, queue management, walk-in booking, manage services, reports
    ws.py                      /ws/queue/{service_id} live queue socket
```

## How FCFS token booking is enforced

`tokens` has a unique constraint on `(service_id, date, token_number)`. When a
customer books a token, the API inserts the row directly; if two requests race
for the same token, the database itself rejects the second `INSERT` with an
integrity error, which the API turns into:

```
409 Conflict — "Token 21 has just been booked by another customer. Please choose another available token."
```

This is safer than a "check then insert" pattern, which has a race window.

## Key endpoints

| Method | Path | Notes |
|---|---|---|
| POST | `/auth/register` | body includes `role`: `customer` or `organization` (+ org fields if organization) |
| POST | `/auth/login-json` | JSON login, returns JWT |
| GET | `/domains` | list of domains with organizations |
| GET | `/organizations?domain=Hospital` | orgs under a domain |
| GET | `/organizations/{id}/services` | services for an org |
| GET | `/services/{id}` | service detail incl. availability + wait time |
| POST | `/services/{id}/book` | customer books a specific token number (FCFS) |
| GET | `/services/{id}/live-queue` | one-off snapshot |
| WS | `/ws/queue/{id}` | live queue updates pushed on every change |
| GET | `/bookings/history` | customer's bookings |
| GET | `/organization/dashboard` | org dashboard stats |
| GET/POST | `/organization/queue/{id}`, `/call-next`, `/skip`, `/complete` | queue management |
| POST | `/organization/walk-in` | book a token on behalf of a walk-in customer |
| GET/POST/PUT/DELETE | `/organization/services` | manage services |
| GET | `/organization/reports` | today's bookings, completed/cancelled, peak hour, most booked service |

All `/organization/*` and customer booking endpoints require `Authorization: Bearer <token>`.
