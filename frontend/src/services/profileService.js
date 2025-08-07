import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

export const profileService = {
  async checkProfileStatus(token) {
    try {
      const response = await axios.get(`${API_BASE_URL}/profile/status`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      return response.data
    } catch (error) {
      console.error('Error checking profile status:', error)
      throw error
    }
  },

  async createStudentProfile(profileData, token) {
    try {
      const response = await axios.post(`${API_BASE_URL}/profile/student`, profileData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      return response.data
    } catch (error) {
      console.error('Error creating student profile:', error)
      throw error
    }
  },

  async createTeacherProfile(profileData, token) {
    try {
      const response = await axios.post(`${API_BASE_URL}/profile/teacher`, profileData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      return response.data
    } catch (error) {
      console.error('Error creating teacher profile:', error)
      throw error
    }
  },

  async createParentProfile(profileData, token) {
    try {
      const response = await axios.post(`${API_BASE_URL}/profile/parent`, profileData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      return response.data
    } catch (error) {
      console.error('Error creating parent profile:', error)
      throw error
    }
  },

  async getStudentProfileStatus(token) {
    try {
      const response = await axios.get(`${API_BASE_URL}/student/profile/status`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      return response.data
    } catch (error) {
      console.error('Error getting student profile status:', error)
      throw error
    }
  },

  async getTeacherProfileStatus(token) {
    try {
      const response = await axios.get(`${API_BASE_URL}/teacher/profile/status`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      return response.data
    } catch (error) {
      console.error('Error getting teacher profile status:', error)
      throw error
    }
  },

  async getParentProfileStatus(token) {
    try {
      const response = await axios.get(`${API_BASE_URL}/parent/profile/status`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      return response.data
    } catch (error) {
      console.error('Error getting parent profile status:', error)
      throw error
    }
  }
} 