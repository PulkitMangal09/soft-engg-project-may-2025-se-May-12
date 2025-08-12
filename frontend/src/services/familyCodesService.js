import axios from 'axios';
const API = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const familyCodesService = {
  async list(token) {
    const { data } = await axios.get(`${API}/parent/family/codes/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return data
  },

  async create(payload, token) {
    // payload: { target_id, expires_at, max_uses }
    const { data } = await axios.post(`${API}/parent/family/codes/`, payload, {
      headers: { Authorization: `Bearer ${token}` }
    })
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
