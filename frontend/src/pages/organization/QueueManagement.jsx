import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getQueue, callNext, skipCurrent, completeCurrent } from '../../api/organization.js'
import { getErrorMessage } from '../../utils/error.js'
import StatusPill from '../../components/StatusPill.jsx'

export default function QueueManagement() {
  const { serviceId } = useParams()
  const [snapshot, setSnapshot] = useState(null)
  const [actionError, setActionError] = useState('')
  const [busy, setBusy] = useState(false)

  const load = () => getQueue(serviceId).then(setSnapshot).catch(() => {})

  useEffect(() => {
    load()
    const interval = setInterval(load, 5000)
    return () => clearInterval(interval)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [serviceId])

  const runAction = async (fn) => {
    setBusy(true)
    setActionError('')
    try {
      await fn(serviceId)
      await load()
    } catch (err) {
      setActionError(getErrorMessage(err, 'Action could not be completed.'))
    } finally {
      setBusy(false)
    }
  }

  const handleRefresh = async () => {
    setBusy(true)
    setActionError('')
    try {
      await getQueue(serviceId).then(setSnapshot)
    } catch (err) {
      setActionError(getErrorMessage(err, 'Failed to refresh queue.'))
    } finally {
      setTimeout(() => setBusy(false), 300)
    }
  }

  if (!snapshot) return <div className="mx-auto max-w-4xl px-6 py-10 text-sm text-slate">Loading queue…</div>

  const serving = snapshot.queue.find((t) => t.status === 'serving')

  return (
    <div className="mx-auto max-w-4xl px-6 py-10">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-sm text-slate">Queue management</p>
          <h1 className="text-2xl font-bold">{snapshot.service_name}</h1>
        </div>
        <div className="flex gap-2">
          <Link to={`/org/services?edit=${serviceId}`} className="btn-secondary">Edit service</Link>
          <Link to={`/org/walk-in?service=${serviceId}`} className="btn-secondary">+ Walk-in booking</Link>
        </div>
      </div>

      {actionError && <p className="mt-4 rounded-lg bg-danger/10 px-3 py-2 text-sm text-danger">{actionError}</p>}

      <div className="card mt-6 flex flex-wrap items-center justify-between gap-6">
        <div className="flex items-center gap-4">
          <span className="ticket-badge-lg">{snapshot.current_token || '—'}</span>
          <div>
            <p className="text-xs font-semibold uppercase text-slate">Now serving</p>
            <p className="text-sm text-slate">{serving ? (serving.customer_name || 'Customer') : 'No one currently'}</p>
          </div>
        </div>
        <div className="flex flex-wrap gap-2">
          <button className="btn-secondary" disabled={busy} onClick={() => runAction(skipCurrent)}>Skip Token</button>
          <button className="btn-secondary" disabled={busy} onClick={() => runAction(completeCurrent)}>Complete Token</button>
          <button className="btn-primary" disabled={busy} onClick={() => runAction(callNext)}>Call Next</button>
          <button className="btn-secondary min-w-[90px]" disabled={busy} onClick={handleRefresh}>
            {busy ? 'Refreshing...' : 'Refresh'}
          </button>
        </div>
      </div>

      <h2 className="mt-8 text-base font-bold">Today's queue</h2>
      <div className="mt-4 overflow-hidden rounded-card border border-slate-200">
        <table className="w-full text-sm">
          <thead className="bg-navy-50 text-left text-xs font-semibold uppercase text-slate">
            <tr>
              <th className="px-4 py-3">Token</th>
              <th className="px-4 py-3">Customer</th>
              <th className="px-4 py-3">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 bg-white">
            {snapshot.queue.map((t) => (
              <tr key={t.token_id}>
                <td className="px-4 py-3 font-mono font-bold text-navy">{t.token_number}</td>
                <td className="px-4 py-3 text-navy-400">
                  {t.customer_name || 'Customer'} {t.is_walk_in && <span className="text-xs text-slate">(walk-in)</span>}
                </td>
                <td className="px-4 py-3"><StatusPill status={t.status} /></td>
              </tr>
            ))}
            {snapshot.queue.length === 0 && (
              <tr><td colSpan={3} className="px-4 py-6 text-center text-slate">No tokens waiting.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
