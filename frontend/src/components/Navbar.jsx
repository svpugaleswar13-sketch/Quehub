import { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

export default function Navbar() {
  const { user, signOut } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const handleSignOut = () => {
    signOut()
    setIsMenuOpen(false)
    navigate('/login')
  }

  const isHome = ['/', '/dashboard', '/org/dashboard', '/login', '/register'].includes(location.pathname)
  const homeLink = user?.role === 'organization' ? '/org/dashboard' : '/dashboard'

  return (
    <>
      <header className="sticky top-0 z-20 border-b border-slate-200 bg-white/90 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-3">
          <div className="flex items-center">
            {/* Sidebar toggle button (hamburger) */}
            {user && (
              <button 
                onClick={() => setIsMenuOpen(true)}
                className="mr-3 flex items-center justify-center h-9 w-9 rounded-lg text-slate hover:bg-slate-100 hover:text-navy transition"
                title="Open Menu"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            )}

            {/* Back button */}
            {user && !isHome && (
              <button 
                onClick={() => navigate(-1)} 
                className="mr-3 flex items-center justify-center h-9 w-9 rounded-lg text-slate hover:bg-slate-100 hover:text-navy transition"
                title="Go Back"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
                </svg>
              </button>
            )}

            <Link to={user ? homeLink : '/'} className="flex items-center gap-2">
              <span className="ticket-badge-sm !h-9 !w-9 !text-xs">QH</span>
              <span className="font-display text-lg font-bold text-navy">QueueHub</span>
            </Link>
          </div>

          {user ? (
            <div className="flex items-center gap-4">
              <div className="hidden items-center gap-4 md:flex">
                {user.role === 'customer' && (
                  <>
                    <Link to="/dashboard" className="text-sm font-medium text-navy-400 hover:text-brand">Dashboard</Link>
                    <Link to="/bookings" className="text-sm font-medium text-navy-400 hover:text-brand">My Bookings</Link>
                  </>
                )}
                {user.role === 'organization' && (
                  <>
                    <Link to="/org/dashboard" className="text-sm font-medium text-navy-400 hover:text-brand">Dashboard</Link>
                    <Link to="/org/services" className="text-sm font-medium text-navy-400 hover:text-brand">Services</Link>
                    <Link to="/org/reports" className="text-sm font-medium text-navy-400 hover:text-brand">Reports</Link>
                  </>
                )}
              </div>
              <span className="hidden text-sm text-slate sm:inline">{user.name}</span>
              <button onClick={handleSignOut} className="btn-secondary !py-1.5 !px-3 text-xs">
                Sign out
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-3">
              <Link to="/login" className="text-sm font-medium text-navy-400 hover:text-brand">Log in</Link>
              <Link to="/register" className="btn-primary !py-1.5 !px-4 text-xs">Get started</Link>
            </div>
          )}
        </div>
      </header>

      {/* Sidebar Backdrop Overlay */}
      {isMenuOpen && (
        <div 
          onClick={() => setIsMenuOpen(false)}
          className="fixed inset-0 z-40 bg-navy-900/30 backdrop-blur-sm animate-fade-in"
        />
      )}

      {/* Left Sidebar Menu */}
      <div 
        className={`fixed top-0 bottom-0 left-0 z-50 w-72 bg-white/95 backdrop-blur-md border-r border-slate-200/50 shadow-2xl flex flex-col justify-between p-6 transition-transform duration-300 ease-in-out ${
          isMenuOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div>
          {/* Sidebar Header */}
          <div className="flex items-center justify-between border-b border-slate-100 pb-5">
            <Link to={user ? homeLink : '/'} onClick={() => setIsMenuOpen(false)} className="flex items-center gap-2">
              <span className="ticket-badge-sm !h-9 !w-9 !text-xs">QH</span>
              <span className="font-display text-lg font-bold text-navy">QueueHub</span>
            </Link>
            <button 
              onClick={() => setIsMenuOpen(false)}
              className="rounded-lg p-1.5 text-slate hover:bg-slate-100 hover:text-navy transition"
              title="Close Menu"
            >
              ✕
            </button>
          </div>

          {/* User Details Profile Card */}
          {user && (
            <div className="mt-6 rounded-xl border border-slate-100 bg-slate-50/50 p-4">
              <p className="text-xs font-bold uppercase tracking-wider text-brand">
                {user.role === 'organization' ? '🏢 Organization' : '👤 Customer'}
              </p>
              <p className="mt-1 font-bold text-navy truncate">{user.name}</p>
              <p className="text-xs text-slate truncate">{user.email}</p>
            </div>
          )}

          {/* Navigation Links */}
          <nav className="mt-8 space-y-2">
            {user?.role === 'customer' && (
              <>
                <Link 
                  to="/dashboard" 
                  onClick={() => setIsMenuOpen(false)}
                  className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-semibold text-navy hover:bg-brand-50 hover:text-brand transition"
                >
                  <span>🏠</span> Dashboard
                </Link>
                <Link 
                  to="/bookings" 
                  onClick={() => setIsMenuOpen(false)}
                  className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-semibold text-navy hover:bg-brand-50 hover:text-brand transition"
                >
                  <span>📅</span> My Bookings
                </Link>
              </>
            )}
            {user?.role === 'organization' && (
              <>
                <Link 
                  to="/org/dashboard" 
                  onClick={() => setIsMenuOpen(false)}
                  className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-semibold text-navy hover:bg-brand-50 hover:text-brand transition"
                >
                  <span>📊</span> Dashboard
                </Link>
                <Link 
                  to="/org/services" 
                  onClick={() => setIsMenuOpen(false)}
                  className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-semibold text-navy hover:bg-brand-50 hover:text-brand transition"
                >
                  <span>⚙️</span> Manage Services
                </Link>
                <Link 
                  to="/org/reports" 
                  onClick={() => setIsMenuOpen(false)}
                  className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-semibold text-navy hover:bg-brand-50 hover:text-brand transition"
                >
                  <span>📈</span> Analytics & Reports
                </Link>
              </>
            )}
          </nav>
        </div>

        {/* Sidebar Footer Sign Out button */}
        {user && (
          <button 
            onClick={handleSignOut}
            className="flex w-full items-center justify-center gap-2 rounded-xl bg-slate-50 border border-slate-200 px-4 py-3 text-sm font-semibold text-slate hover:bg-danger/10 hover:text-danger hover:border-danger/20 transition duration-200"
          >
            <span>🚪</span> Sign Out
          </button>
        )}
      </div>
    </>
  )
}
