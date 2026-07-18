import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { listOrganizations } from '../../api/customer.js'

export default function DomainOrganizations() {
  const { domain } = useParams()
  const [orgs, setOrgs] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    listOrganizations(domain).then(setOrgs).finally(() => setLoading(false))
  }, [domain])

  return (
    <div className="mx-auto max-w-6xl px-6 py-10">
      <p className="text-sm text-slate">Domain</p>
      <h1 className="text-2xl font-bold">{domain}</h1>

      {loading && <p className="mt-6 text-sm text-slate">Loading organizations…</p>}
      {!loading && orgs.length === 0 && (
        <p className="mt-6 text-sm text-slate">No organizations found under {domain} yet.</p>
      )}

      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        {orgs.map((org) => (
          <Link key={org.id} to={`/organizations/${org.id}`} className="card transition hover:shadow-card-hover">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-base font-bold text-navy">{org.name}</h3>
                <p className="mt-1 text-sm text-slate">{org.address}</p>
              </div>
              {org.rating > 0 && (
                <span className="rounded-full bg-warning/15 px-2.5 py-1 text-xs font-semibold text-warning">★ {org.rating}</span>
              )}
            </div>
            <p className="mt-3 text-xs font-medium text-slate">{org.working_hours}</p>
          </Link>
        ))}
      </div>
    </div>
  )
}
