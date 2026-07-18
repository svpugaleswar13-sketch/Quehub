import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { getBookingHistory } from '../../api/customer.js'
import StatusPill from '../../components/StatusPill.jsx'

const TABS = [
  { key: 'all', label: 'All' },
  { key: 'waiting', label: 'Upcoming' },
  { key: 'completed', label: 'Completed' },
  { key: 'cancelled', label: 'Cancelled' },
]

export default function BookingHistory() {
  const [bookings, setBookings] = useState([])
  const [tab, setTab] = useState('all')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getBookingHistory().then(setBookings).finally(() => setLoading(false))
  }, [])

  const filtered = useMemo(
    () => (tab === 'all' ? bookings : bookings.filter((b) => b.status === tab)),
    [bookings, tab],
  )

  return (
    <div className="mx-auto max-w-4xl px-6 py-10">
      <h1 className="text-2xl font-bold">My Bookings</h1>

      <div className="mt-6 flex gap-2 border-b border-slate-200">
        {TABS.map((t) => (
          <button
            key={t.key}
            onClick={() => setTab(t.key)}
            className={`border-b-2 px-3 py-2 text-sm font-semibold transition ${
              tab === t.key ? 'border-brand text-brand' : 'border-transparent text-slate hover:text-navy'
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div className="mt-6 space-y-3">
        {loading && <p className="text-sm text-slate">Loading…</p>}
        {!loading && filtered.length === 0 && <p className="text-sm text-slate">No bookings here yet.</p>}
        {filtered.map((b) => (
          <Link
            key={b.booking_id}
            to={b.status === 'waiting' ? `/live-queue/${b.service_id}` : '#'}
            state={{ myToken: b.token_number }}
            className={`card flex items-center gap-4 transition block ${
              b.status === 'waiting' ? 'hover:shadow-card-hover cursor-pointer' : 'cursor-default'
            }`}
          >
            <span className="ticket-badge">{b.token_number}</span>
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-bold text-navy">{b.organization_name}</p>
              <p className="truncate text-xs text-slate">{b.service_name}</p>
              <p className="mt-1 text-xs text-slate">{new Date(b.booking_time).toLocaleString()}</p>
            </div>
            <StatusPill status={b.status} />
          </Link>
        ))}
      </div>
    </div>
  )
}
