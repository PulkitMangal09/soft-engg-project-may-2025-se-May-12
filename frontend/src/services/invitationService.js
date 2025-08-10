import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

export const invitationService = {
  // POST /codes/generate - Generate invitation code
  async generateCode(codeData, token) {
    try {
      const response = await axios.post(`${API_BASE_URL}/codes/generate`, codeData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      return response.data
    } catch (error) {
      console.error('Error generating invitation code:', error)
      throw error
    }
  },

  // GET /codes/my - List my invitation codes
  async getMyInvitationCodes(token, targetType = null) {
    try {
      const params = targetType ? { target_type: targetType } : {}
      const response = await axios.get(`${API_BASE_URL}/codes/my`, {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        params
      })
      return response.data
    } catch (error) {
      console.error('Error fetching invitation codes:', error)
      throw error
    }
  },

  // POST /requests/redeem - Redeem invitation code (for students/parents)
  async redeemCode(code, token) {
    try {
      const response = await axios.post(`${API_BASE_URL}/requests/redeem`, { code }, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      return response.data
    } catch (error) {
      console.error('Error redeeming invitation code:', error)
      throw error
    }
  },

  // GET /requests/pending - List pending join requests
  async getPendingRequests(token) {
    try {
      const response = await axios.get(`${API_BASE_URL}/requests/pending`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      return response.data
    } catch (error) {
      console.error('Error fetching pending requests:', error)
      throw error
    }
  },

  // POST /requests/{request_id}/approve - Approve join request
  async approveRequest(requestId, token) {
    try {
      const response = await axios.post(`${API_BASE_URL}/requests/${requestId}/approve`, {}, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      return response.data
    } catch (error) {
      console.error('Error approving request:', error)
      throw error
    }
  },

  // POST /requests/{request_id}/reject - Reject join request
  async rejectRequest(requestId, token) {
    try {
      const response = await axios.post(`${API_BASE_URL}/requests/${requestId}/reject`, {}, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      return response.data
    } catch (error) {
      console.error('Error rejecting request:', error)
      throw error
    }
  }
}
