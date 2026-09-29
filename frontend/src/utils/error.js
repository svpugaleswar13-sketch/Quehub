export function getErrorMessage(err, fallback) {
  if (!err) return fallback || 'An unknown error occurred'

  if (err.code === 'ECONNABORTED' || (err.message && err.message.toLowerCase().includes('timeout'))) {
    return 'Request timed out. Please check if the backend server is running and try again.'
  }

  if (!err.response) {
    if (err.message === 'Network Error' || err.code === 'ERR_NETWORK') {
      return 'Cannot connect to the backend server. Please ensure the backend server is running at http://localhost:8000.'
    }
    return err.message || fallback
  }

  const { status, data } = err.response
  if (status >= 500) {
    return `Server error (${status}). Please check backend logs or try again later.`
  }

  const detail = data?.detail
  if (!detail) return fallback
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail.map((d) => d.msg || JSON.stringify(d)).join(', ')
  }
  return fallback
}


