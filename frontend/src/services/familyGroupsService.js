// src/services/familyGroupsService.js
import axios from 'axios'
const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export const familyGroupsService = {
  async list(token) {
    const { data } = await axios.get(`${API}/parent/family/groups`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return data
  },

  async create(payload, token) {
    // payload: { name, description }
    const { data } = await axios.post(`${API}/parent/family/groups`, payload, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return data
  },

  async update(groupId, payload, token) {
    const { data } = await axios.patch(`${API}/parent/family/groups/${groupId}`, payload, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return data
  },

  async remove(groupId, token) {
    const { data } = await axios.delete(`${API}/parent/family/groups/${groupId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return data
  },
}
