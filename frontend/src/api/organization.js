import client from './client'

export const getDashboard = () => client.get('/organization/dashboard').then((r) => r.data)

export const getQueue = (serviceId) =>
  client.get(`/organization/queue/${serviceId}`).then((r) => r.data)

export const callNext = (serviceId) =>
  client.post(`/organization/queue/${serviceId}/call-next`).then((r) => r.data)

export const skipCurrent = (serviceId) =>
  client.post(`/organization/queue/${serviceId}/skip`).then((r) => r.data)

export const completeCurrent = (serviceId) =>
  client.post(`/organization/queue/${serviceId}/complete`).then((r) => r.data)

export const walkInBooking = (payload) =>
  client.post('/organization/walk-in', payload).then((r) => r.data)

export const listOwnServices = () => client.get('/organization/services').then((r) => r.data)

export const createService = (payload) =>
  client.post('/organization/services', payload).then((r) => r.data)

export const updateService = (serviceId, payload) =>
  client.put(`/organization/services/${serviceId}`, payload).then((r) => r.data)

export const deleteService = (serviceId) =>
  client.delete(`/organization/services/${serviceId}`)

export const getReports = () => client.get('/organization/reports').then((r) => r.data)
