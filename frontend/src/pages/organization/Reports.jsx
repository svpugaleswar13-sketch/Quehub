import { useEffect, useState } from 'react'
import { getReports } from '../../api/organization.js'
import StatCard from '../../components/StatCard.jsx'

export default function Reports() {
  const [report, setReport] = useState(null)

  useEffect(() => { getReports().then(setReport) }, [])

  if (!report) return <div className="mx-auto max-w-4xl px-6 py-10 text-sm text-slate">Loading…</div>

  return (
    <div className="mx-auto max-w-4xl px-6 py-10">
      <h1 className="text-2xl font-bold">Reports</h1>
      <p className="mt-1 text-sm text-slate">Today's activity across all services.</p>

      <div className="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-3">
        <StatCard label="Today's bookings" value={report.todays_bookings} />
        <StatCard label="Completed tokens" value={report.completed_tokens} accent="text-success" />
        <StatCard label="Cancelled tokens" value={report.cancelled_tokens} accent="text-danger" />
        <StatCard label="Avg. waiting time" value={`${report.average_waiting_time_minutes}m`} />
        <StatCard label="Most booked service" value={report.most_booked_service || '—'} />
        <StatCard label="Peak hour" value={report.peak_hour || '—'} />
      </div>
    </div>
  )
}
