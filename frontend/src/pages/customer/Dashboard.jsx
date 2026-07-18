import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { listDomains, getNotifications, getBookingHistory } from '../../api/customer.js'
import { useAuth } from '../../context/AuthContext.jsx'
import StatusPill from '../../components/StatusPill.jsx'

const DOMAIN_ICONS = {
  Hospital: '🏥', Bank: '🏦', Salon: '💇', Spa: '💆',
  'Government Office': '🏛️', 'Passport Office': '🛂', 'Vehicle Service Center': '🚗',
  Government: '🏛️', Education: '🎓',
}

export default function CustomerDashboard() {
  const { user } = useAuth()
  const [domains, setDomains] = useState([])
  const [notifications, setNotifications] = useState([])
  const [bookings, setBookings] = useState([])
  const [search, setSearch] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    listDomains().then(setDomains).catch(() => {})
    getNotifications().then(setNotifications).catch(() => {})
    getBookingHistory().then(setBookings).catch(() => {})
  }, [])

  const handleSearch = (e) => {
    e.preventDefault()
    if (search.trim()) navigate(`/domains/${encodeURIComponent(search.trim())}`)
  }

  const upcoming = bookings.filter((b) => b.status === 'waiting').slice(0, 4)
  const recent = bookings.slice(0, 4)

  return (
    <div className="mx-auto max-w-6xl px-6 py-10">
      <h1 className="text-2xl font-bold">Hi {user?.name?.split(' ')[0]}, where to today?</h1>
      <p className="mt-1 text-sm text-slate">Search for an organization or browse by category.</p>

      <form onSubmit={handleSearch} className="mt-6 flex gap-2">
        <input
          className="input"
          placeholder="Search a domain, e.g. Hospital"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <button type="submit" className="btn-primary shrink-0">Search</button>
      </form>

      <h2 className="mt-10 text-lg font-bold">Browse by category</h2>
      <div className="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4">
        {domains.map((d) => (
          <Link
            key={d}
            to={`/domains/${encodeURIComponent(d)}`}
            className="card flex flex-col items-center gap-2 py-6 text-center transition hover:shadow-card-hover"
          >
            <span className="text-3xl">{DOMAIN_ICONS[d] || '📍'}</span>
            <span className="text-sm font-semibold text-navy">{d}</span>
          </Link>
        ))}
      </div>

      <div className="mt-10 grid gap-6 md:grid-cols-2">
        <div>
          <h2 className="text-lg font-bold">Upcoming bookings</h2>
          <div className="mt-4 space-y-3">
            {upcoming.length === 0 && <p className="text-sm text-slate">No upcoming bookings yet.</p>}
            {upcoming.map((b) => (
              <Link
                key={b.booking_id}
                to={`/live-queue/${b.service_id}`}
                state={{ myToken: b.token_number }}
                className="card flex items-center gap-4 py-4 transition hover:shadow-card-hover block cursor-pointer"
              >
                <span className="ticket-badge-sm">{b.token_number}</span>
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-semibold text-navy">{b.organization_name}</p>
                  <p className="truncate text-xs text-slate">{b.service_name}</p>
                </div>
                <StatusPill status={b.status} />
              </Link>
            ))}
          </div>
        </div>

        <div>
          <h2 className="text-lg font-bold">Notifications</h2>
          <div className="mt-4 space-y-3">
            {notifications.length === 0 && <p className="text-sm text-slate">You're all caught up.</p>}
            {notifications.slice(0, 5).map((n) => (
              <div key={n.id} className={`card py-3 text-sm ${n.read_status ? 'text-slate' : 'font-medium text-navy'}`}>
                {n.message}
              </div>
            ))}
          </div>
        </div>
      </div>

      {recent.length > 0 && (
        <div className="mt-10">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold">Recent bookings</h2>
            <Link to="/bookings" className="text-sm font-semibold text-brand hover:underline">View all</Link>
          </div>
          <div className="mt-4 space-y-3">
            {recent.map((b) => (
              <div key={b.booking_id} className="card flex items-center gap-4 py-4">
                <span className="ticket-badge-sm">{b.token_number}</span>
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-semibold text-navy">{b.organization_name} — {b.service_name}</p>
                </div>
                <StatusPill status={b.status} />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
