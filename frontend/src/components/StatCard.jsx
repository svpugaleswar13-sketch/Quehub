export default function StatCard({ label, value, accent = 'text-navy' }) {
  return (
    <div className="card">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate">{label}</p>
      <p className={`mt-2 font-display text-3xl font-bold ${accent}`}>{value}</p>
    </div>
  )
}
