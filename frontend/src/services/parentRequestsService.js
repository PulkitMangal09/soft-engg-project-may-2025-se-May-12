import axios from 'axios'
const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const asBearer = (t) => (typeof t === 'string' ? t : t?.access_token || t?.token || '')
const withAuth = (t) => ({ headers: { Authorization: `Bearer ${asBearer(t)}` } })

export const parentRequestsService = {
  async listPending(token) {
    const { data } = await axios.get(`${API}/parent/requests/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return data
  },
  async list(token) {
    const { data } = await axios.get(`${API}/parent/requests/`, withAuth(token))
    return data
  },
  async approve(requestId, token) {
    const { data } = await axios.post(`${API}/parent/requests/${requestId}/approve`, {}, withAuth(token))
    return data
  },
  async reject(requestId, token) {
    const { data } = await axios.post(`${API}/parent/requests/${requestId}/reject`, {}, withAuth(token))
    return data
  }
}