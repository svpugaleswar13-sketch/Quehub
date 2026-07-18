import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { getServiceDetail, bookToken } from '../../api/customer.js'
import { getErrorMessage } from '../../utils/error.js'

export default function ServiceDetails() {
  const { serviceId } = useParams()
  const [detail, setDetail] = useState(null)
  const [selected, setSelected] = useState(null)
  const [booking, setBooking] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const load = () => getServiceDetail(serviceId).then(setDetail).catch(() => {})

  useEffect(() => {
    load()
    // Light polling keeps the token grid fresh without a websocket on this page;
    // the dedicated Live Queue page after booking uses a real socket.
    const interval = setInterval(load, 8000)
    return () => clearInterval(interval)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [serviceId])

  const handleBook = async () => {
    if (!selected) return
    setBooking(true)
    setError('')
    try {
      const result = await bookToken(serviceId, selected)
      navigate('/booking-success', { state: { result, serviceId } })
    } catch (err) {
      setError(getErrorMessage(err, 'Could not book that token. Please try another.'))
      setSelected(null)
      load()
    } finally {
      setBooking(false)
    }
  }

  if (!detail) return <div className="mx-auto max-w-4xl px-6 py-10 text-sm text-slate">Loading…</div>

  const { service, current_token, available_token_numbers, estimated_waiting_time_minutes, booked_tokens } = detail
  const takenSet = new Set(Array.from({ length: service.max_tokens }, (_, i) => i + 1).filter((n) => !available_token_numbers.includes(n)))

  return (
    <div className="mx-auto max-w-4xl px-6 py-10">
      <h1 className="text-2xl font-bold">{service.name}</h1>
      <p className="mt-1 text-sm text-slate">{service.start_time?.slice(0, 5)} – {service.end_time?.slice(0, 5)}</p>

      <div className="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-4">
        <div className="card py-4 text-center">
          <p className="text-xs font-semibold uppercase text-slate">Current token</p>
          <p className="mt-1 font-mono text-2xl font-bold text-brand-700">{current_token ?? '—'}</p>
        </div>
        <div className="card py-4 text-center">
          <p className="text-xs font-semibold uppercase text-slate">Booked</p>
          <p className="mt-1 font-mono text-2xl font-bold text-navy">{booked_tokens}</p>
        </div>
        <div className="card py-4 text-center">
          <p className="text-xs font-semibold uppercase text-slate">Available</p>
          <p className="mt-1 font-mono text-2xl font-bold text-success">{available_token_numbers.length}</p>
        </div>
        <div className="card py-4 text-center">
          <p className="text-xs font-semibold uppercase text-slate">Avg. wait</p>
          <p className="mt-1 font-mono text-2xl font-bold text-navy">{service.average_service_time}m</p>
        </div>
      </div>

      <h2 className="mt-8 text-base font-bold">Choose an available token</h2>
      {error && <p className="mt-3 rounded-lg bg-danger/10 px-3 py-2 text-sm text-danger">{error}</p>}

      <div className="mt-4 flex flex-wrap gap-3">
        {Array.from({ length: service.max_tokens }, (_, i) => i + 1).map((n) => {
          const isTaken = takenSet.has(n)
          const isSelected = selected === n
          return (
            <button
              key={n}
              disabled={isTaken}
              onClick={() => setSelected(n)}
              className={[
                isTaken ? 'ticket-badge ticket-badge-taken' : 'ticket-badge ticket-badge-selectable',
                isSelected ? '!border-brand !bg-brand !text-white' : '',
              ].join(' ')}
            >
              {n}
            </button>
          )
        })}
      </div>

      <div className="mt-8 flex items-center justify-between rounded-card border border-slate-200 bg-white p-5">
        <div>
          <p className="text-sm text-slate">Selected token</p>
          <p className="font-mono text-xl font-bold text-navy">{selected ?? '—'}</p>
        </div>
        <button className="btn-primary" disabled={!selected || booking} onClick={handleBook}>
          {booking ? 'Booking…' : 'Book Token'}
        </button>
      </div>

      <p className="mt-3 text-xs text-slate">
        Estimated wait if you book the next token now: ~{estimated_waiting_time_minutes} minutes.
      </p>
    </div>
  )
}
