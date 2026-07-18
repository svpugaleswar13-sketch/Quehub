import client from './client'

export function register(payload) {
  return client.post('/auth/register', payload).then((res) => res.data)
}

export function login(email, password) {
  return client.post('/auth/login-json', { email, password }).then((res) => res.data)
}
