import { Link, useLocation, useNavigate } from 'react-router-dom'

export default function BookingSuccess() {
  const { state } = useLocation()
  const navigate = useNavigate()

  if (!state?.result) {
    return (
      <div className="mx-auto max-w-lg px-6 py-16 text-center">
        <p className="text-sm text-slate">No booking to show.</p>
        <Link to="/dashboard" className="mt-4 inline-block text-sm font-semibold text-brand hover:underline">Back to dashboard</Link>
      </div>
    )
  }

  const { result, serviceId } = state

  return (
    <div className="mx-auto max-w-lg px-6 py-14 text-center">
      <span className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-success/15 text-2xl text-success">✓</span>
      <h1 className="mt-4 text-2xl font-bold">Booking successful</h1>
      <p className="mt-1 text-sm text-slate">{result.organization_name} · {result.service_name}</p>

      <div className="card mt-8 flex flex-col items-center gap-4">
        <span className="ticket-badge-lg !h-24 !w-24 !text-4xl">{result.token_number}</span>

        <div className="grid w-full grid-cols-2 gap-4 text-left">
          <div>
            <p className="text-xs font-semibold uppercase text-slate">Current token</p>
            <p className="font-mono text-lg font-bold text-navy">{result.current_token ?? '—'}</p>
          </div>
          <div>
            <p className="text-xs font-semibold uppercase text-slate">Customers before you</p>
            <p className="font-mono text-lg font-bold text-navy">{result.customers_before_you}</p>
          </div>
          <div>
            <p className="text-xs font-semibold uppercase text-slate">Estimated wait</p>
            <p className="font-mono text-lg font-bold text-navy">{result.estimated_waiting_time_minutes}m</p>
          </div>
          <div>
            <p className="text-xs font-semibold uppercase text-slate">Status</p>
            <p className="text-lg font-bold capitalize text-brand">{result.status}</p>
          </div>
        </div>
      </div>

      <div className="mt-8 flex justify-center gap-3">
        <button className="btn-primary" onClick={() => navigate(`/live-queue/${serviceId}`, { state: { myToken: result.token_number } })}>
          Track live queue
        </button>
        <Link to="/dashboard" className="btn-secondary">Back to dashboard</Link>
      </div>
    </div>
  )
}
