import { createContext, useContext, useState, useCallback } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem('queuehub_user')
    return stored ? JSON.parse(stored) : null
  })

  const signIn = useCallback((accessToken, userData) => {
    localStorage.setItem('queuehub_token', accessToken)
    localStorage.setItem('queuehub_user', JSON.stringify(userData))
    setUser(userData)
  }, [])

  const signOut = useCallback(() => {
    localStorage.removeItem('queuehub_token')
    localStorage.removeItem('queuehub_user')
    setUser(null)
  }, [])

  return (
    <AuthContext.Provider value={{ user, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
