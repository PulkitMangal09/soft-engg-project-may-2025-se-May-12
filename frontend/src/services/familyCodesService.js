import axios from 'axios';
const API = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const asBearer = (t) => (typeof t === 'string' ? t : t?.access_token || t?.token || '')
const withAuth = (t) => ({ headers: { Authorization: `Bearer ${asBearer(t)}` } })

export const familyCodesService = {
  async list(token) {
    const { data } = await axios.get(`${API}/parent/family/codes/`, withAuth(token))
    return data
  },
  async create(payload, token) {
    const { data } = await axios.post(`${API}/parent/family/codes/`, payload, withAuth(token))
    return data
  },

  // POST /parent/family/codes/{code_id}/revoke
  async revoke(code_id, token) {
    const { data } = await axios.post(
      `${API}/parent/family/codes/${code_id}/revoke`,
      {},
      { headers: { Authorization: `Bearer ${token}` } }
    );
    return data;
  }
};
