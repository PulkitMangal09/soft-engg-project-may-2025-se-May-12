import axios from 'axios'
const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const familyGroupsService = {
  async listGroups(token) {
    const { data } = await axios.get(`${API}/parent/family/groups`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return data
  },

  async joinViaCode({ family_code, role, message }, token) {
    const { data } = await axios.post(`${API}/parent/family/join`,
      { family_code, role, message },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    return data
  },
}
