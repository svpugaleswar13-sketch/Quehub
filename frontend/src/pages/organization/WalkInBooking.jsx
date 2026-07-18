import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { listOwnServices, getQueue, walkInBooking } from '../../api/organization.js'
import { getErrorMessage } from '../../utils/error.js'

export default function WalkInBooking() {
  const [searchParams] = useSearchParams()
  const [services, setServices] = useState([])
  const [serviceId, setServiceId] = useState(searchParams.get('service') || '')
  const [queueSnapshot, setQueueSnapshot] = useState(null)
  const [name, setName] = useState('')
  const [phone, setPhone] = useState('')
  const [selectedToken, setSelectedToken] = useState(null)
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    listOwnServices().then((data) => {
      setServices(data)
      if (!serviceId && data.length > 0) setServiceId(data[0].id)
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    if (!serviceId) return
    getQueue(serviceId).then(setQueueSnapshot)
  }, [serviceId])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!selectedToken) return
    setSubmitting(true)
    setError('')
    try {
      await walkInBooking({ customer_name: name, customer_phone: phone || undefined, service_id: serviceId, token_number: selectedToken })
      navigate(`/org/queue/${serviceId}`)
    } catch (err) {
      setError(getErrorMessage(err, 'Could not book this token.'))
      setSelectedToken(null)
      getQueue(serviceId).then(setQueueSnapshot)
    } finally {
      setSubmitting(false)
    }
  }

  const service = services.find((s) => s.id === serviceId)
  const takenSet = new Set(
    service && queueSnapshot
      ? Array.from({ length: service.max_tokens }, (_, i) => i + 1).filter((n) => !queueSnapshot.available_token_numbers.includes(n))
      : [],
  )

  return (
    <div className="mx-auto max-w-2xl px-6 py-10">
      <h1 className="text-2xl font-bold">Walk-in Booking</h1>
      <p className="mt-1 text-sm text-slate">Book a token for a customer visiting in person.</p>

      <form onSubmit={handleSubmit} className="card mt-6 space-y-4">
        {error && <p className="rounded-lg bg-danger/10 px-3 py-2 text-sm text-danger">{error}</p>}

        <div>
          <label className="label">Customer name</label>
          <input className="input" required value={name} onChange={(e) => setName(e.target.value)} placeholder="Ramesh" />
        </div>
        <div>
          <label className="label">Mobile number (optional)</label>
          <input className="input" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="98765 43210" />
        </div>
        <div>
          <label className="label">Service</label>
          <select className="input" value={serviceId} onChange={(e) => { setServiceId(e.target.value); setSelectedToken(null) }}>
            {services.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
          </select>
        </div>

        {service && queueSnapshot && (
          <div>
            <label className="label">Available tokens</label>
            <div className="flex flex-wrap gap-2">
              {Array.from({ length: service.max_tokens }, (_, i) => i + 1).map((n) => {
                const isTaken = takenSet.has(n)
                const isSelected = selectedToken === n
                return (
                  <button
                    type="button"
                    key={n}
                    disabled={isTaken}
                    onClick={() => setSelectedToken(n)}
                    className={[
                      isTaken ? 'ticket-badge-sm ticket-badge-taken' : 'ticket-badge-sm ticket-badge-selectable',
                      isSelected ? '!border-brand !bg-brand !text-white' : '',
                    ].join(' ')}
                  >
                    {n}
                  </button>
                )
              })}
            </div>
          </div>
        )}

        <button type="submit" className="btn-primary w-full" disabled={!selectedToken || submitting}>
          {submitting ? 'Booking…' : 'Book'}
        </button>
      </form>
    </div>
  )
}
