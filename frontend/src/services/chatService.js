import axios from 'axios'

const API = axios

export async function createSession(sessionType, sessionTitle = null) {
  const body = { session_type: sessionType }
  if (sessionTitle) body.session_title = sessionTitle
  const { data } = await API.post('/student/emotions/sessions', body)
  return data
}

export async function getMessages(sessionId) {
  const { data } = await API.get(`/student/emotions/messages/${sessionId}`)
  return data || []
}

export async function autoReply(sessionId, userMessage) {
  const form = new FormData()
  if (userMessage) form.append('user_message', userMessage)
  const { data } = await API.post(`/student/emotions/sessions/${sessionId}/auto-reply`, form, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  return data
}

export async function autoReplyWithImage(sessionId, userMessage, file) {
  const form = new FormData()
  if (userMessage) form.append('user_message', userMessage)
  if (file) form.append('file', file)
  const { data } = await API.post(`/student/emotions/sessions/${sessionId}/auto-reply`, form, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  return data
}

export async function ensureSession(sessionRef, sessionType, title = null) {
  if (!sessionRef.value) {
    sessionRef.value = await createSession(sessionType, title)
  }
  return sessionRef.value
}

export async function closeSession(sessionId) {
  if (!sessionId) return
  try {
    const body = { is_active: false, ended_at: new Date().toISOString() }
    await API.patch(`/student/emotions/sessions/${sessionId}`, body)
  } catch {
    // swallow errors on close
  }
}

export async function listSessions() {
  const { data } = await API.get('/student/emotions/sessions')
  return (data || []).sort((a, b) => {
    const at = new Date(a.started_at || a.created_at || 0).getTime()
    const bt = new Date(b.started_at || b.created_at || 0).getTime()
    return bt - at
  })
}

export async function reopenSession(sessionId) {
  const { data } = await API.patch(`/student/emotions/sessions/${sessionId}`, {
    is_active: true,
    ended_at: null
  })
  return data
}


