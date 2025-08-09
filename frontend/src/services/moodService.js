import axios from 'axios'

const API = axios

export async function listMoodLogs() {
  const { data } = await API.get('/student/emotions/mood-logs')
  return data || []
}

export async function getMoodLog(id) {
  const { data } = await API.get(`/student/emotions/mood-logs/${id}`)
  return data
}

export async function createMoodLog(payload) {
  // payload can include: mood, energy_level, sleep_quality, stress_level, notes, log_date
  const { data } = await API.post('/student/emotions/mood-logs', payload)
  return data
}

export async function updateMoodLog(id, updates) {
  const { data } = await API.patch(`/student/emotions/mood-logs/${id}`, updates)
  return data
}

export async function deleteMoodLog(id) {
  await API.delete(`/student/emotions/mood-logs/${id}`)
}


