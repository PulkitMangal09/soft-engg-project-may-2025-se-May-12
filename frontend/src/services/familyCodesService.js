import axios from 'axios'
const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const familyCodesService = {
  async list(token) {
    const { data } = await axios.get(`${API}/parent/family/codes`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return data
  },
  async create(payload, token) {
    const { data } = await axios.post(`${API}/parent/family/codes`, payload, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return data
  },
  async revoke(code_id, token) {
    const { data } = await axios.delete(`${API}/parent/family/codes/${code_id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return data
  }
}
