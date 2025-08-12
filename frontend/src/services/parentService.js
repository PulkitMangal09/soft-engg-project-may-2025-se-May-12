// src/services/parentService.js
import { api } from './api'
import axios from 'axios'
const API = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const asBearer = (t) => (typeof t === 'string' ? t : t?.access_token || t?.token || '')
const withAuth = (t) => ({ headers: { Authorization: `Bearer ${asBearer(t)}` } })


export const parentService = {
  // Dashboard (keep if you have these routes)
  async getDashboard() {
    const { data } = await axios.get(`${API}/parent/dashboard/`, withAuth(token))
    return data
  },
  async getTasks() {
    const { data } = await api.get('/parent/dashboard/tasks')
    return data
  },
  async getHealthAlerts() {
    const { data } = await api.get('/parent/dashboard/health/alerts')
    return data
  },

  // Children
  async getChildren() {
    const { data } = await axios.get(`${API}/parent/children`, withAuth(token))
    return data
  },
  async getChildrenMetrics() {
    const { data } = await api.get('/parent/children/metrics')
    return data
  },

  // Family groups
  async getFamilyOverview() {
    const { data } = await api.get('/parent/family/overview')
    return data
  },
  async getFamilyGroups() {
    const { data } = await api.get('/parent/family/groups')
    return data
  },
  async createFamilyGroup(groupData) {
    const { data } = await api.post('/parent/family/groups', groupData)
    return data
  },

  // *** Requests (now use /requests router) ***
  async getFamilyJoinRequests() {
    const { data } = await axios.get(`${API}/parent/requests/`, withAuth(token))
    return data
  },
  async respondToFamilyJoinRequest(requestId, action /* 'approve'|'reject' */) {
    // unified handler expects 'accept'|'reject'
    const { data } = await axios.post(`${API}/parent/requests/${id}/${action}`, {}, withAuth(token))
    return data
  },
}

export default parentService
