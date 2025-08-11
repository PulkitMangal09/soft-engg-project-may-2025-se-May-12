import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
})

// Parent Dashboard APIs
export const parentService = {
  // GET /parent/dashboard/ - Get Parent Dashboard
  async getDashboard(token) {
    try {
      const response = await api.get('/parent/dashboard/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    } catch (error) {
      console.error('Error fetching parent dashboard:', error)
      throw error
    }
  },

  // GET /parent/dashboard/tasks - Get Parent Tasks
  async getTasks(token) {
    try {
      const response = await api.get('/parent/dashboard/tasks', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    } catch (error) {
      console.error('Error fetching parent tasks:', error)
      throw error
    }
  },

  // GET /parent/dashboard/health/alerts - Get Parent Health Alerts
  async getHealthAlerts(token) {
    try {
      const response = await api.get('/parent/dashboard/health/alerts', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    } catch (error) {
      console.error('Error fetching health alerts:', error)
      throw error
    }
  },

  // GET /parent/dashboard/family/join-requests - Get Family Join Requests
  async getFamilyJoinRequests(token) {
    try {
      const response = await api.get('/parent/dashboard/family/join-requests', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    } catch (error) {
      console.error('Error fetching family join requests:', error)
      throw error
    }
  },

  // POST /parent/dashboard/family/join-requests/respond - Respond Family Join Request
  async respondToFamilyJoinRequest(requestId, action, token) {
    try {
      const response = await api.post('/parent/dashboard/family/join-requests/respond', {
        request_id: requestId,
        action: action // 'approve' or 'reject'
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    } catch (error) {
      console.error('Error responding to family join request:', error)
      throw error
    }
  },

  // GET /parent/children - Get Children
  async getChildren(token) {
    try {
      const response = await api.get('/parent/children', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    } catch (error) {
      console.error('Error fetching children:', error)
      throw error
    }
  },

  // GET /parent/children/metrics - View All Children Metrics
  async getChildrenMetrics(token) {
    try {
      const response = await api.get('/parent/children/metrics', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    } catch (error) {
      console.error('Error fetching children metrics:', error)
      throw error
    }
  },

  // GET /parent/family/overview - Family Overview
  async getFamilyOverview(token) {
    try {
      const response = await api.get('/parent/family/overview', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    } catch (error) {
      console.error('Error fetching family overview:', error)
      throw error
    }
  },

  // GET /parent/family/groups - List Family Groups
  async getFamilyGroups(token) {
    try {
      const response = await api.get('/parent/family/groups', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    } catch (error) {
      console.error('Error fetching family groups:', error)
      throw error
    }
  },

  // POST /parent/family/groups - Create Family Group
  async createFamilyGroup(groupData, token) {
    try {
      const response = await api.post('/parent/family/groups', groupData, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    } catch (error) {
      console.error('Error creating family group:', error)
      throw error
    }
  }
}

export default parentService
