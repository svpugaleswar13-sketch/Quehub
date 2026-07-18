const STYLES = {
  waiting: 'bg-brand-50 text-brand-700',
  serving: 'bg-warning/15 text-warning',
  completed: 'bg-success/15 text-success',
  skipped: 'bg-slate-200 text-slate',
  cancelled: 'bg-danger/15 text-danger',
}

export default function StatusPill({ status }) {
  const style = STYLES[status] || 'bg-slate-200 text-slate'
  return (
    <span className={`status-pill ${style}`}>
      {status?.charAt(0).toUpperCase() + status?.slice(1)}
    </span>
  )
}
