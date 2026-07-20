import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { login } from '../api/auth.js'
import { useAuth } from '../context/AuthContext.jsx'
import { getErrorMessage } from '../utils/error.js'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { signIn } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const data = await login(email, password)
      signIn(data.access_token, data.user)
      navigate(data.user.role === 'organization' ? '/org/dashboard' : '/dashboard')
    } catch (err) {
      setError(getErrorMessage(err, 'Could not sign in. Check your details and try again.'))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto flex min-h-[80vh] max-w-md flex-col justify-center px-6 py-12">
      <div className="mb-8 text-center">
        <span className="ticket-badge-lg mx-auto">Q</span>
        <h1 className="mt-4 text-2xl font-bold">Welcome backs</h1>
        <p className="mt-1 text-sm text-slate">Log in to book tokens or manage your queue.</p>
      </div>

      <form onSubmit={handleSubmit} className="card space-y-4">
        {error && <p className="rounded-lg bg-danger/10 px-3 py-2 text-sm text-danger">{error}</p>}
        <div>
          <label className="label">Email</label>
          <input className="input" type="email" required value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" />
        </div>
        <div>
          <label className="label">Password</label>
          <input className="input" type="password" required value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" />
        </div>
        <button type="submit" className="btn-primary w-full" disabled={loading}>
          {loading ? 'Signing in…' : 'Log in'}
        </button>
      </form>

      <p className="mt-6 text-center text-sm text-slate">
        Don't have an account?{' '}
        <Link to="/register" className="font-semibold text-brand hover:underline">Register</Link>
      </p>
    </div>
  )
}
