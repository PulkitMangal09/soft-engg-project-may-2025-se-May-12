// src/services/parentService.js
import { api } from './api'

export const parentService = {
  // Dashboard (keep if you have these routes)
  async getDashboard() {
    const { data } = await api.get('/parent/dashboard')
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
    const { data } = await api.get('/parent/children')
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
    // pending for approver (family head)
    const { data } = await api.get('/requests/pending')
    return data
  },
  async respondToFamilyJoinRequest(requestId, action /* 'approve'|'reject' */) {
    // unified handler expects 'accept'|'reject'
    const payload = { action: action === 'approve' ? 'accept' : 'reject' }
    const { data } = await api.patch(`/requests/${requestId}/handle`, payload)
    return data
  },
}

export default parentService
