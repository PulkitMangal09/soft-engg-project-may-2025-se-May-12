import axios from 'axios'
const API = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const asBearer = (t) => (typeof t === 'string' ? t : t?.access_token || t?.token || '')
const withAuth = (t) => ({ headers: { Authorization: `Bearer ${asBearer(t)}` } })

export const familyGroupsService = {
  // groups where I'm the head
  async listHeaded(token) {
    const { data } = await axios.get(`${API}/parent/family/groups`, withAuth(token))
    return data
  },

  // alias for old call sites
  async listGroups(token) { return this.listHeaded(token) },

  // groups where I'm a member (joined/approved)
  async listMemberships(token) {
    const { data } = await axios.get(`${API}/parent/family/memberships`, withAuth(token))
    return data
  },

  async get(groupId, token) {
    const { data } = await axios.get(`${API}/parent/family/groups/${groupId}`, withAuth(token))
    return data
  },

  async create({ name, description }, token) {
    const { data } = await axios.post(`${API}/parent/family/groups`, { name, description }, withAuth(token))
    return data
  },

  async update(groupId, { name, description }, token) {
    const { data } = await axios.patch(`${API}/parent/family/groups/${groupId}`, { name, description }, withAuth(token))
    return data
  },

  async remove(groupId, token) {
    const { data } = await axios.delete(`${API}/parent/family/groups/${groupId}`, withAuth(token))
    return data
  },
}
