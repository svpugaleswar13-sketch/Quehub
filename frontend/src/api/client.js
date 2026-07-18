import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const client = axios.create({
  baseURL: API_URL,
})

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('queuehub_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const { status, data } = error.response
      // Clear session and redirect if token is expired/invalid (401) or role mismatch (403)
      if (
        status === 401 ||
        (status === 403 &&
          (data?.detail === 'Customer access required' ||
            data?.detail === 'Organization access required'))
      ) {
        localStorage.removeItem('queuehub_token')
        localStorage.removeItem('queuehub_user')
        if (window.location.pathname !== '/login') {
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  }
)

export const WS_URL = API_URL.replace(/^http/, 'ws')

export default client

