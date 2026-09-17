export function getErrorMessage(err, fallback) {
  if (!err.response) {
    if (err.message === 'Network Error' || err.code === 'ERR_NETWORK') {
      return 'Cannot connect to the server. Please check your internet connection or ensure the backend server is running on port 8000.'
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
    return detail.map((d) => d.msg).join(', ')
  }
  return fallback
}

