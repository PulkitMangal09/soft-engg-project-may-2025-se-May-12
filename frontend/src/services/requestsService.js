// /src/services/requestsService.js
import axios from 'axios'
const API_BASE_URL = import.meta.env?.VITE_API_BASE_URL || 'http://localhost:8000'
const api = axios.create({ baseURL: API_BASE_URL })

export async function listRequests(token, status = 'pending') {
  const { data } = await api.get(`/teacher/requests`, {
    params: { status },
    headers: { Authorization: `Bearer ${token}` },
  })
  return data || []
}

export async function respondToRequest(id, action, token) {
  const { data } = await api.patch(`/teacher/requests/${id}`, { action }, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return data
}

export const requestsService = { listRequests, respondToRequest }
export default requestsService
