const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
async function request(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, { headers: { 'Content-Type': 'application/json' }, ...options })
  if (!response.ok) { const body = await response.json().catch(() => ({})); throw new Error(body.detail || 'Something went wrong.') }
  return response.status === 204 ? null : response.json()
}
export const api = {
  dashboard: () => request('/dashboard/stats'), reports: () => request('/reports/summary'),
  tickets: (params = {}) => request(`/tickets?${new URLSearchParams(Object.entries(params).filter(([, v]) => v)).toString()}`),
  createTicket: body => request('/tickets', { method: 'POST', body: JSON.stringify(body) }), updateTicket: (id, body) => request(`/tickets/${id}`, { method: 'PUT', body: JSON.stringify(body) }), deleteTicket: id => request(`/tickets/${id}`, { method: 'DELETE' }),
  assets: (params = {}) => request(`/assets?${new URLSearchParams(Object.entries(params).filter(([, v]) => v)).toString()}`),
  createAsset: body => request('/assets', { method: 'POST', body: JSON.stringify(body) }), updateAsset: (id, body) => request(`/assets/${id}`, { method: 'PUT', body: JSON.stringify(body) }), deleteAsset: id => request(`/assets/${id}`, { method: 'DELETE' }),
  users: (params = {}) => request(`/users?${new URLSearchParams(Object.entries(params).filter(([, v]) => v)).toString()}`),
  createUser: body => request('/users', { method: 'POST', body: JSON.stringify(body) }), updateUser: (id, body) => request(`/users/${id}`, { method: 'PUT', body: JSON.stringify(body) }), deleteUser: id => request(`/users/${id}`, { method: 'DELETE' })
}
