import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getOrganization, listServices } from '../../api/customer.js'

export default function OrganizationPage() {
  const { organizationId } = useParams()
  const [org, setOrg] = useState(null)
  const [services, setServices] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    Promise.all([getOrganization(organizationId), listServices(organizationId)])
      .then(([orgData, servicesData]) => {
        setOrg(orgData)
        setServices(servicesData)
      })
      .finally(() => setLoading(false))
  }, [organizationId])

  if (loading) return <div className="mx-auto max-w-6xl px-6 py-10 text-sm text-slate">Loading…</div>
  if (!org) return <div className="mx-auto max-w-6xl px-6 py-10 text-sm text-slate">Organization not found.</div>

  return (
    <div className="mx-auto max-w-6xl px-6 py-10">
      <div className="card">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-brand">{org.domain}</p>
            <h1 className="mt-1 text-2xl font-bold">{org.name}</h1>
            <p className="mt-2 text-sm text-slate">{org.address}</p>
          </div>
          {org.rating > 0 && (
            <span className="rounded-full bg-warning/15 px-3 py-1.5 text-sm font-semibold text-warning">★ {org.rating}</span>
          )}
        </div>
        <p className="mt-4 text-sm font-medium text-navy-400">Working hours: {org.working_hours}</p>
      </div>

      <h2 className="mt-8 text-lg font-bold">Available services</h2>
      <div className="mt-4 grid gap-4 sm:grid-cols-2 md:grid-cols-3">
        {services.map((s) => (
          <Link key={s.id} to={`/services/${s.id}`} className="card transition hover:shadow-card-hover">
            <h3 className="font-bold text-navy">{s.name}</h3>
            <p className="mt-1 text-xs text-slate">{s.start_time?.slice(0, 5)} – {s.end_time?.slice(0, 5)}</p>
            <p className="mt-3 text-xs font-medium text-brand">View availability →</p>
          </Link>
        ))}
        {services.length === 0 && <p className="text-sm text-slate">No services listed yet.</p>}
      </div>
    </div>
  )
}
