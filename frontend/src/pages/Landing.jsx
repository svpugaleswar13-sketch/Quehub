import { Link } from 'react-router-dom'

const DOMAINS = ['Hospitals', 'Banks', 'Salons & Spas', 'Government Offices', 'Passport Offices', 'Vehicle Service Centers', 'Government Agencies', 'Educational Institutions']

export default function Landing() {
  return (
    <div>
      <section className="mx-auto max-w-3xl px-6 pb-20 pt-16 text-center sm:pt-24">
        <span className="inline-flex items-center rounded-full bg-brand-50 px-3 py-1 text-xs font-semibold text-brand-700">
          Digital token queues
        </span>
        <h1 className="mt-4 font-display text-4xl font-extrabold leading-tight text-navy sm:text-5xl">
          Take a number.<br />Skip the waiting room.
        </h1>
        <p className="mx-auto mt-4 max-w-md text-base text-slate">
          QueueHub replaces the physical line with a live token queue. Pick your slot,
          watch it move in real time, and walk in exactly when it's your turn.
        </p>
        <div className="mt-8 flex justify-center gap-3">
          <Link to="/login" className="btn-primary">Log in</Link>
          <Link to="/register" className="btn-secondary">Register</Link>
        </div>
      </section>

      <section className="border-t border-slate-200 bg-white py-14">
        <div className="mx-auto max-w-6xl px-6">
          <h2 className="text-center text-sm font-semibold uppercase tracking-wide text-slate">Built for any token-based queue</h2>
          <div className="mt-6 flex flex-wrap justify-center gap-3">
            {DOMAINS.map((d) => (
              <span key={d} className="rounded-full border border-slate-200 bg-bg px-4 py-2 text-sm font-medium text-navy-400">
                {d}
              </span>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
