import axios from 'axios';

function getAuthHeader() {
  const raw = (localStorage.getItem('token') || '').trim();
  if (!raw) return null;
  // Accept "bearer <jwt>", "Bearer <jwt>" or "<jwt>"
  const jwt = raw.replace(/^bearer\s+/i, '').replace(/^Bearer\s+/i, '');
  return `Bearer ${jwt}`;
}

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
});

api.interceptors.request.use((cfg) => {
  const auth = getAuthHeader();
  if (auth) cfg.headers.Authorization = auth;
  return cfg;
});

export default api;
