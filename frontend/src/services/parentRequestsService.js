import axios from 'axios'
const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const parentRequestsService = {
  async listPending(token) {
    const { data } = await axios.get(`${API}/parent/requests/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return data
  },
  async approve(request_id, token) {
    const { data } = await axios.post(`${API}/parent/requests/${request_id}/approve`, null, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return data
  },
  async reject(request_id, token) {
    const { data } = await axios.post(`${API}/parent/requests/${request_id}/reject`, null, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return data
  }
}
