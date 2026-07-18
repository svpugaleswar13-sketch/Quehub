import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { listOwnServices, createService, updateService, deleteService } from '../../api/organization.js'
import { getErrorMessage } from '../../utils/error.js'

const EMPTY_FORM = { name: '', start_time: '09:00', end_time: '17:00', max_tokens: 40, average_service_time: 10 }

export default function ManageServices() {
  const [services, setServices] = useState([])
  const [form, setForm] = useState(EMPTY_FORM)
  const [editingId, setEditingId] = useState(null)
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)
  const [searchParams, setSearchParams] = useSearchParams()

  const load = () => listOwnServices().then((data) => { setServices(data); return data })

  const startEdit = (s) => {
    setEditingId(s.id)
    setForm({
      name: s.name,
      start_time: s.start_time.slice(0, 5),
      end_time: s.end_time.slice(0, 5),
      max_tokens: s.max_tokens,
      average_service_time: s.average_service_time,
    })
  }

  const cancelEdit = () => {
    setEditingId(null)
    setForm(EMPTY_FORM)
    // Clear the edit param from URL
    const newParams = new URLSearchParams(searchParams)
    newParams.delete('edit')
    setSearchParams(newParams)
  }

  useEffect(() => {
    load().then((loadedServices) => {
      const editId = searchParams.get('edit')
      if (editId && loadedServices) {
        const s = loadedServices.find((x) => x.id === editId)
        if (s) {
          startEdit(s)
        }
      }
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams])

  const update = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    setError('')
    const payload = {
      name: form.name,
      start_time: `${form.start_time}:00`,
      end_time: `${form.end_time}:00`,
      max_tokens: Number(form.max_tokens),
      average_service_time: Number(form.average_service_time),
    }
    try {
      if (editingId) {
        await updateService(editingId, payload)
      } else {
        await createService(payload)
      }
      cancelEdit()
      await load()
    } catch (err) {
      setError(getErrorMessage(err, 'Could not save this service.'))
    } finally {
      setSaving(false)
    }
  }

  const toggleActive = async (s) => {
    await updateService(s.id, { is_active: !s.is_active })
    load()
  }

  const remove = async (s) => {
    if (!confirm(`Delete "${s.name}"? This cannot be undone.`)) return
    await deleteService(s.id)
    load()
  }

  return (
    <div className="mx-auto max-w-4xl px-6 py-10">
      <h1 className="text-2xl font-bold">Manage Services</h1>

      <form onSubmit={handleSubmit} className="card mt-6 space-y-4">
        <h2 className="text-base font-bold">{editingId ? 'Edit service' : 'Add service'}</h2>
        {error && <p className="rounded-lg bg-danger/10 px-3 py-2 text-sm text-danger">{error}</p>}

        <div>
          <label className="label">Service name</label>
          <input className="input" required value={form.name} onChange={update('name')} placeholder="Dentist" />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="label">Start time</label>
            <input className="input" type="time" required value={form.start_time} onChange={update('start_time')} />
          </div>
          <div>
            <label className="label">End time</label>
            <input className="input" type="time" required value={form.end_time} onChange={update('end_time')} />
          </div>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="label">Maximum tokens</label>
            <input className="input" type="number" min="1" required value={form.max_tokens} onChange={update('max_tokens')} />
          </div>
          <div>
            <label className="label">Average service time (minutes)</label>
            <input className="input" type="number" min="1" required value={form.average_service_time} onChange={update('average_service_time')} />
          </div>
        </div>

        <div className="flex gap-2">
          <button type="submit" className="btn-primary" disabled={saving}>
            {saving ? 'Saving…' : editingId ? 'Save changes' : 'Add service'}
          </button>
          {editingId && <button type="button" className="btn-secondary" onClick={cancelEdit}>Cancel</button>}
        </div>
      </form>

      <h2 className="mt-10 text-lg font-bold">Your services</h2>
      <div className="mt-4 space-y-3">
        {services.map((s) => (
          <div key={s.id} className="card flex flex-wrap items-center justify-between gap-4">
            <div>
              <p className="font-bold text-navy">{s.name}</p>
              <p className="text-xs text-slate">
                {s.start_time.slice(0, 5)}–{s.end_time.slice(0, 5)} · {s.max_tokens} tokens · {s.average_service_time}m avg
              </p>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              <span className={`status-pill ${s.is_active ? 'bg-success/15 text-success' : 'bg-slate-200 text-slate'}`}>
                {s.is_active ? 'Active' : 'Disabled'}
              </span>
              <button className="btn-secondary !py-1.5 !px-3 text-xs" onClick={() => startEdit(s)}>Edit</button>
              <button className="btn-secondary !py-1.5 !px-3 text-xs" onClick={() => toggleActive(s)}>
                {s.is_active ? 'Disable' : 'Enable'}
              </button>
              <button className="btn-danger !py-1.5 !px-3 text-xs" onClick={() => remove(s)}>Delete</button>
            </div>
          </div>
        ))}
        {services.length === 0 && <p className="text-sm text-slate">No services yet — add your first one above.</p>}
      </div>
    </div>
  )
}
