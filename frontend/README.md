# QueueHub Frontend (React + Vite + Tailwind)

## Setup

```bash
cd frontend
npm install
cp .env.example .env      # points VITE_API_URL at the backend, defaults to localhost:8000
npm run dev
```

Opens at http://localhost:5173. Requires the backend running (see `backend/README.md`).

## Design system

- **Colors** — navy (`#14203D`) for headings/nav, brand blue (`#2C6BED`) for actions, a
  soft `#F5F7FB` page background. All defined in `tailwind.config.js`.
- **Type** — Sora for headings, Inter for body copy, JetBrains Mono for anything
  numeric (token numbers, stats).
- **Signature element** — the `.ticket-badge` classes in `src/index.css`: a
  dashed-border "ticket" badge used everywhere a token number appears (token
  grid, booking success, live queue, org queue table), echoing a real
  deli/bank-counter paper token.

## Structure

```
src/
  api/                axios client + one file per API area (auth, customer, organization)
  context/AuthContext.jsx   JWT + user stored in localStorage, read by ProtectedRoute
  components/           Navbar, ProtectedRoute, StatCard, StatusPill
  pages/
    Landing.jsx, Login.jsx, Register.jsx
    customer/            Dashboard, DomainOrganizations, OrganizationPage, ServiceDetails,
                          BookingSuccess, LiveQueue (WebSocket), BookingHistory
    organization/          Dashboard, QueueManagement (call next/skip/complete), WalkInBooking,
                            ManageServices (CRUD + enable/disable), Reports
```

## Notes

- `ServiceDetails` and `QueueManagement` poll the REST snapshot every 5–8s so the
  token grid stays fresh even before a booking exists to watch over a socket.
  `LiveQueue` (used after a booking) opens a real WebSocket to `/ws/queue/{id}`
  for instant updates.
- Auth token is stored in `localStorage` under `queuehub_token` — fine for this
  scaffold; consider httpOnly cookies for production hardening.
