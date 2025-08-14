import axios from 'axios'
const API = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const asBearer = (t) => (typeof t === 'string' ? t : t?.access_token || t?.token || '')
const withAuth = (t) => ({ headers: { Authorization: `Bearer ${asBearer(t)}` } })

export const parentAnalyticsService = {
  async getDashboard(token, params = {}) {
    const { data } = await axios.get(`${API}/parent/dashboard/`, { ...withAuth(token), params })
    return data
  },
  async getTasks(token, params = {}) {
    const { data } = await axios.get(`${API}/parent/dashboard/tasks`, { ...withAuth(token), params })
    return data
  },
  async createTask(token, payload) {
    const { data } = await axios.post(`${API}/parent/tasks`, payload, withAuth(token))
    return data
  },
  async getGoals(token, params = {}) {
    const { data } = await axios.get(`${API}/parent/dashboard/finance/goals`, { ...withAuth(token), params })
    return data
  },
  async getTransactions(token, params = {}) {
    const { data } = await axios.get(`${API}/parent/dashboard/finance/transactions`, { ...withAuth(token), params })
    return data
  },
}
