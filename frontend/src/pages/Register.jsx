import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { register } from '../api/auth.js'
import { useAuth } from '../context/AuthContext.jsx'
import { getErrorMessage } from '../utils/error.js'

const DOMAINS = ['Hospital', 'Bank', 'Salon', 'Spa', 'Government Office', 'Passport Office', 'Vehicle Service Center', 'Government', 'Education']

export default function Register() {
  const [role, setRole] = useState('customer')
  const [form, setForm] = useState({
    name: '', email: '', password: '',
    organization_name: '', domain: DOMAINS[0], address: '', working_hours: '09:00 AM - 05:00 PM',
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { signIn } = useAuth()
  const navigate = useNavigate()

  const update = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const payload = { name: form.name, email: form.email, password: form.password, role }
      if (role === 'organization') {
        Object.assign(payload, {
          organization_name: form.organization_name,
          domain: form.domain,
          address: form.address,
          working_hours: form.working_hours,
        })
      }
      const data = await register(payload)
      signIn(data.access_token, data.user)
      navigate(role === 'organization' ? '/org/dashboard' : '/dashboard')
    } catch (err) {
      const fallback = role === 'organization'
        ? 'Could not create organization account. Please check your details.'
        : 'Could not create customer account. Please check your details.'
      setError(getErrorMessage(err, fallback))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto flex min-h-[80vh] max-w-md flex-col justify-center px-6 py-12">
      <div className="mb-6 text-center">
        <h1 className="text-2xl font-bold">Create your account</h1>
        <p className="mt-1 text-sm text-slate">Book tokens as a customer, or manage a queue as an organization.</p>
      </div>

      <div className="mb-6 grid grid-cols-2 gap-2 rounded-lg bg-navy-50 p-1">
        <button
          type="button"
          onClick={() => setRole('customer')}
          className={`rounded-md py-2 text-sm font-semibold transition ${role === 'customer' ? 'bg-white text-brand shadow-card' : 'text-navy-400'}`}
        >
          Customer
        </button>
        <button
          type="button"
          onClick={() => setRole('organization')}
          className={`rounded-md py-2 text-sm font-semibold transition ${role === 'organization' ? 'bg-white text-brand shadow-card' : 'text-navy-400'}`}
        >
          Organization
        </button>
      </div>

      <form onSubmit={handleSubmit} className="card space-y-4">
        {error && <p className="rounded-lg bg-danger/10 px-3 py-2 text-sm text-danger">{error}</p>}

        <div>
          <label className="label">{role === 'organization' ? 'Admin name' : 'Full name'}</label>
          <input className="input" required value={form.name} onChange={update('name')} placeholder="Your name" />
        </div>
        <div>
          <label className="label">Email</label>
          <input className="input" type="email" required value={form.email} onChange={update('email')} placeholder="you@example.com" />
        </div>
        <div>
          <label className="label">Password</label>
          <input className="input" type="password" required minLength={6} value={form.password} onChange={update('password')} placeholder="At least 6 characters" />
        </div>

        {role === 'organization' && (
          <>
            <hr className="border-slate-200" />
            <div>
              <label className="label">Organization name</label>
              <input className="input" required value={form.organization_name} onChange={update('organization_name')} placeholder="Apollo Hospital" />
            </div>
            <div>
              <label className="label">Domain</label>
              <select className="input" value={form.domain} onChange={update('domain')}>
                {DOMAINS.map((d) => <option key={d} value={d}>{d}</option>)}
              </select>
            </div>
            <div>
              <label className="label">Address</label>
              <input className="input" value={form.address} onChange={update('address')} placeholder="Street, city" />
            </div>
            <div>
              <label className="label">Working hours</label>
              <input className="input" value={form.working_hours} onChange={update('working_hours')} placeholder="09:00 AM - 05:00 PM" />
            </div>
          </>
        )}

        <button type="submit" className="btn-primary w-full" disabled={loading}>
          {loading ? 'Creating account…' : 'Create account'}
        </button>
      </form>

      <p className="mt-6 text-center text-sm text-slate">
        Already have an account?{' '}
        <Link to="/login" className="font-semibold text-brand hover:underline">Log in</Link>
      </p>
    </div>
  )
}
