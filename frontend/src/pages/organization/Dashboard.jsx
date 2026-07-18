import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getDashboard, listOwnServices, getQueue } from '../../api/organization.js'
import StatCard from '../../components/StatCard.jsx'
import StatusPill from '../../components/StatusPill.jsx'

export default function OrganizationDashboard() {
  const [stats, setStats] = useState(null)
  const [services, setServices] = useState([])
  const [queues, setQueues] = useState({})
  const [activeModal, setActiveModal] = useState(null) // 'all' | 'serving' | 'completed' | 'pending' | 'cancelled' | null

  useEffect(() => {
    getDashboard().then(setStats).catch(() => {})
    listOwnServices().then((data) => {
      setServices(data)
      data.forEach((s) => {
        getQueue(s.id)
          .then((q) => {
            setQueues((prev) => ({ ...prev, [s.id]: q }))
          })
          .catch(() => {})
      })
    }).catch(() => {})
  }, [])

  const getModalData = () => {
    if (!activeModal) return { title: '', tokens: [] }

    let title = ''
    let statusFilter = []

    if (activeModal === 'all') {
      title = "Today's Bookings"
      statusFilter = ['completed', 'waiting', 'serving', 'skipped', 'cancelled']
    } else if (activeModal === 'serving') {
      title = 'Currently Serving'
      statusFilter = ['serving']
    } else if (activeModal === 'completed') {
      title = 'Completed Bookings'
      statusFilter = ['completed']
    } else if (activeModal === 'pending') {
      title = 'Pending Bookings'
      statusFilter = ['waiting', 'serving']
    } else if (activeModal === 'cancelled') {
      title = 'Cancelled & Skipped'
      statusFilter = ['cancelled', 'skipped']
    }

    const tokens = services
      .flatMap((s) => {
        const q = queues[s.id]
        const list = q?.queue?.filter((t) => statusFilter.includes(t.status)) || []
        return list.map((t) => ({ service: s, token: t }))
      })
      .sort((a, b) => a.token.token_number - b.token.token_number)

    return { title, tokens }
  }

  const getBadgeStyle = (status) => {
    if (status === 'completed') return '!bg-success/10 !border-success/30 !text-success'
    if (status === 'cancelled' || status === 'skipped') return '!bg-danger/10 !border-danger/30 !text-danger'
    return '!bg-warning/10 !border-warning/30 !text-warning'
  }

  const { title: modalTitle, tokens: modalTokens } = getModalData()

  return (
    <div className="mx-auto max-w-6xl px-6 py-10">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <p className="mt-1 text-sm text-slate">Today's overview across all services.</p>

      {stats && (
        <div className="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-6">
          <button onClick={() => setActiveModal('all')} className="block transition hover:scale-[1.02] text-left w-full focus:outline-none">
            <StatCard label="Today's bookings" value={stats.todays_bookings} />
          </button>
          <button onClick={() => setActiveModal('serving')} className="block transition hover:scale-[1.02] text-left w-full focus:outline-none">
            <StatCard label="Current token" value={stats.current_token ?? '—'} accent="text-brand-700" />
          </button>
          <button onClick={() => setActiveModal('completed')} className="block transition hover:scale-[1.02] text-left w-full focus:outline-none">
            <StatCard label="Completed" value={stats.completed_tokens} accent="text-success" />
          </button>
          <button onClick={() => setActiveModal('pending')} className="block transition hover:scale-[1.02] text-left w-full focus:outline-none">
            <StatCard label="Pending" value={stats.pending_tokens} accent="text-warning" />
          </button>
          <button onClick={() => setActiveModal('cancelled')} className="block transition hover:scale-[1.02] text-left w-full focus:outline-none">
            <StatCard label="Cancelled" value={stats.cancelled_tokens} accent="text-danger" />
          </button>
          <div className="block">
            <StatCard label="Avg. wait" value={`${stats.average_waiting_time_minutes}m`} />
          </div>
        </div>
      )}

      {/* Details Modal */}
      {activeModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-navy-900/40 p-4 backdrop-blur-sm animate-fade-in">
          <div className="w-full max-w-lg rounded-2xl border border-slate-100 bg-white p-6 shadow-xl animate-scale-in">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
              <h2 className="text-lg font-bold">{modalTitle}</h2>
              <button 
                onClick={() => setActiveModal(null)}
                className="rounded-lg p-1 text-slate hover:bg-slate-100 transition"
              >
                ✕
              </button>
            </div>
            
            <div className="mt-4 space-y-4 max-h-[60vh] overflow-y-auto pr-1">
              {modalTokens.length === 0 ? (
                <div className="text-center py-6">
                  <p className="text-sm text-slate">No tokens found for this category.</p>
                  <p className="text-xs text-slate-400 mt-1">Updates will display here automatically.</p>
                </div>
              ) : (
                modalTokens.map(({ service, token }) => (
                  <div key={token.token_id} className="flex items-center gap-4 rounded-xl border border-slate-100 bg-slate-50/50 p-4 hover:border-brand/20 transition">
                    <span className={`ticket-badge-sm !h-12 !w-12 !border-solid font-semibold ${getBadgeStyle(token.status)}`}>
                      {token.token_number}
                    </span>
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2">
                        <p className="font-bold text-sm text-navy truncate">{service.name}</p>
                        <StatusPill status={token.status} />
                      </div>
                      <p className="text-xs text-slate mt-1">
                        {token.customer_name || 'Customer'} {token.is_walk_in && '(Walk-in)'}
                      </p>
                    </div>
                    <Link 
                      to={`/org/queue/${service.id}`} 
                      className="btn-primary !py-1.5 !px-3 !text-xs shrink-0"
                      onClick={() => setActiveModal(null)}
                    >
                      Manage
                    </Link>
                  </div>
                ))
              )}
            </div>
            
            <div className="mt-6 flex justify-end">
              <button 
                onClick={() => setActiveModal(null)}
                className="btn-secondary !py-2 !px-4 !text-sm"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="mt-10 flex items-center justify-between">
        <h2 className="text-lg font-bold">Manage a queue</h2>
        <Link to="/org/services" className="text-sm font-semibold text-brand hover:underline">Manage services →</Link>
      </div>

      <div className="mt-4 grid gap-4 sm:grid-cols-2 md:grid-cols-3">
        {services.map((s) => (
          <Link
            key={s.id}
            to={`/org/queue/${s.id}`}
            className="card flex flex-col justify-between transition hover:shadow-card-hover block cursor-pointer"
          >
            <div>
              <h3 className="font-bold text-navy hover:text-brand transition">{s.name}</h3>
              <p className="mt-1 text-xs text-slate">Max {s.max_tokens} tokens · {s.average_service_time}m avg</p>
            </div>
            <div className="mt-4 flex items-center justify-between" onClick={(e) => e.stopPropagation()}>
              <span className={`text-xs font-semibold ${s.is_active ? 'text-success' : 'text-slate'}`}>
                {s.is_active ? 'Active' : 'Disabled'}
              </span>
              <Link to={`/org/services?edit=${s.id}`} className="text-xs font-semibold text-brand hover:underline">
                Edit service
              </Link>
            </div>
          </Link>
        ))}
        {services.length === 0 && (
          <p className="text-sm text-slate">No services yet — <Link to="/org/services" className="font-semibold text-brand hover:underline">add one</Link> to start taking bookings.</p>
        )}
      </div>
    </div>
  )
}
