// /src/services/invitationService.js
import axios from 'axios'

const API_BASE_URL = import.meta.env?.VITE_API_BASE_URL || 'http://localhost:8000'
const api = axios.create({ baseURL: API_BASE_URL })

/**
 * Generate an invitation code.
 * payload = {
 *   target_type: 'classroom' | 'family',
 *   target_id: string (uuid),
 *   expires_at?: string (ISO),
 *   max_uses?: number | null
 * }
 */
async function generateCode(payload, token) {
  const { data } = await api.post('/codes', payload, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return data
}

/**
 * List my invitation codes (optionally filter by target_type)
 * targetType can be 'classroom' or 'family'
 */
async function getMyInvitationCodes(token, targetType) {
  const url = targetType ? `/codes/my?target_type=${encodeURIComponent(targetType)}` : '/codes/my'
  const { data } = await api.get(url, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return data
}

/** Revoke/delete a code */
async function revokeCode(codeId, token) {
  const { data } = await api.delete(`/codes/${codeId}`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return data
}

export const invitationService = {
  generateCode,
  getMyInvitationCodes,
  revokeCode,
}

export default invitationService
