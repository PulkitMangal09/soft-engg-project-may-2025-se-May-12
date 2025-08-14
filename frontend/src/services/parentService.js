// src/services/parentService.js
import { api } from './api'
import axios from 'axios'
const API = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const asBearer = (t) => (typeof t === 'string' ? t : t?.access_token || t?.token || '')
const withAuth = (t) => ({ headers: { Authorization: `Bearer ${asBearer(t)}` } })


export const parentService = {
  // Dashboard (keep if you have these routes)
  async getDashboard(token) {
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
  async getChildren(token) {
    // Use reports endpoint that lists only student-children
    const { data } = await axios.get(`${API}/parent/reports/students`, withAuth(token))
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
  async getFamilyGroups(token) {
    // If api client auto-injects auth, this is fine; otherwise switch to axios with withAuth(token)
    const { data } = await api.get('/parent/family/groups')
    return data
  },
  async createFamilyGroup(groupData) {
    const { data } = await api.post('/parent/family/groups', groupData)
    return data
  },

  // *** Requests (now use /requests router) ***
  async getFamilyJoinRequests(token) {
    const { data } = await axios.get(`${API}/parent/requests/`, withAuth(token))
    return data
  },
  async respondToFamilyJoinRequest(requestId, action, token) {
    // Map legacy 'approve' to 'accept'
    const mapped = action === 'approve' ? 'accept' : action
    const { data } = await axios.post(`${API}/parent/requests/${requestId}/${mapped}`, {}, withAuth(token))
    return data
  },
}

export default parentService
