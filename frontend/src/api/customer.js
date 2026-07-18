import client from './client'

export const listDomains = () => client.get('/domains').then((r) => r.data)

export const listOrganizations = (domain) =>
  client.get('/organizations', { params: domain ? { domain } : {} }).then((r) => r.data)

export const getOrganization = (organizationId) =>
  client.get(`/organizations/${organizationId}`).then((r) => r.data)

export const listServices = (organizationId) =>
  client.get(`/organizations/${organizationId}/services`).then((r) => r.data)

export const getServiceDetail = (serviceId) =>
  client.get(`/services/${serviceId}`).then((r) => r.data)

export const bookToken = (serviceId, tokenNumber) =>
  client.post(`/services/${serviceId}/book`, { token_number: tokenNumber }).then((r) => r.data)

export const getLiveQueueSnapshot = (serviceId) =>
  client.get(`/services/${serviceId}/live-queue`).then((r) => r.data)

export const getBookingHistory = () => client.get('/bookings/history').then((r) => r.data)

export const getNotifications = () => client.get('/notifications').then((r) => r.data)

export const markNotificationRead = (id) =>
  client.post(`/notifications/${id}/read`).then((r) => r.data)
