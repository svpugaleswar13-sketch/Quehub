import { useEffect, useRef, useState } from 'react'
import { useLocation, useParams } from 'react-router-dom'
import { WS_URL } from '../../api/client.js'
import { getLiveQueueSnapshot } from '../../api/customer.js'
import StatusPill from '../../components/StatusPill.jsx'

export default function LiveQueue() {
  const { serviceId } = useParams()
  const { state } = useLocation()
  const myToken = state?.myToken
  const [snapshot, setSnapshot] = useState(null)
  const [connected, setConnected] = useState(false)
  const wsRef = useRef(null)

  useEffect(() => {
    // Load an initial snapshot over REST in case the socket takes a moment.
    getLiveQueueSnapshot(serviceId).then(setSnapshot).catch(() => {})

    const ws = new WebSocket(`${WS_URL}/ws/queue/${serviceId}`)
    wsRef.current = ws
    ws.onopen = () => setConnected(true)
    ws.onclose = () => setConnected(false)
    ws.onmessage = (event) => {
      try {
        setSnapshot(JSON.parse(event.data))
      } catch {
        // ignore malformed frames
      }
    }
    return () => ws.close()
  }, [serviceId])

  if (!snapshot) return <div className="mx-auto max-w-3xl px-6 py-10 text-sm text-slate">Connecting to live queue…</div>

  const myEntry = snapshot.queue.find((t) => t.token_number === myToken)
  const customersBefore = myToken
    ? snapshot.queue.filter((t) => t.token_number < myToken).length
    : null
  const waitMinutes = customersBefore != null ? customersBefore * snapshot.average_service_time : null

  return (
    <div className="mx-auto max-w-3xl px-6 py-10">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-slate">{snapshot.service_name}</p>
          <h1 className="text-2xl font-bold">Live Queue</h1>
        </div>
        <span className={`status-pill ${connected ? 'bg-success/15 text-success' : 'bg-slate-200 text-slate'}`}>
          {connected ? 'Live' : 'Reconnecting…'}
        </span>
      </div>

      <div className="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-4">
        <div className="card py-4 text-center">
          <p className="text-xs font-semibold uppercase text-slate">Current token</p>
          <p className="mt-1 font-mono text-2xl font-bold text-brand-700">{snapshot.current_token ?? '—'}</p>
        </div>
        {myToken && (
          <div className="card py-4 text-center">
            <p className="text-xs font-semibold uppercase text-slate">Your token</p>
            <p className="mt-1 font-mono text-2xl font-bold text-navy">{myToken}</p>
          </div>
        )}
        {myToken && (
          <div className="card py-4 text-center">
            <p className="text-xs font-semibold uppercase text-slate">Ahead of you</p>
            <p className="mt-1 font-mono text-2xl font-bold text-navy">{customersBefore}</p>
          </div>
        )}
        {myToken && (
          <div className="card py-4 text-center">
            <p className="text-xs font-semibold uppercase text-slate">Est. wait</p>
            <p className="mt-1 font-mono text-2xl font-bold text-navy">{waitMinutes}m</p>
          </div>
        )}
      </div>

      {myEntry && (
        <div className="mt-4 rounded-card border border-brand-100 bg-brand-50 p-4 text-sm font-medium text-brand-700">
          Your status: {myEntry.status === 'serving' ? "You're being served now" : 'Waiting'}
        </div>
      )}

      <h2 className="mt-8 text-base font-bold">Queue</h2>
      <div className="mt-4 space-y-2">
        {snapshot.queue.map((t) => (
          <div
            key={t.token_id}
            className={`flex items-center gap-4 rounded-card border p-3 ${t.token_number === myToken ? 'border-brand bg-brand-50' : 'border-slate-200 bg-white'}`}
          >
            <span className="ticket-badge-sm">{t.token_number}</span>
            <span className="flex-1 text-sm font-medium text-navy">
              {t.token_number === myToken ? 'You' : (t.customer_name || 'Customer')} {t.is_walk_in && <span className="text-xs text-slate">(walk-in)</span>}
            </span>
            <StatusPill status={t.status} />
          </div>
        ))}
        {snapshot.queue.length === 0 && <p className="text-sm text-slate">No one is currently waiting.</p>}
      </div>
    </div>
  )
}
