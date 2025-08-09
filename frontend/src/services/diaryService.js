import axios from 'axios'

const API = axios

function mapEntry(raw) {
  return {
    id: raw.entry_id || raw.id,
    title: raw.title || '',
    content: raw.content || '',
    tags: raw.tags || [],
    date: raw.created_at || raw.date,
  }
}

export async function listDiaryEntries() {
  const { data } = await API.get('/student/emotions/entries')
  return (data || []).map(mapEntry)
}

export async function getDiaryEntry(id) {
  const { data } = await API.get(`/student/emotions/entries/${id}`)
  return mapEntry(data)
}

export async function createDiaryEntry({ title, content, tags }) {
  const payload = { title, content, tags: tags || [] }
  const { data } = await API.post('/student/emotions/entries', payload)
  return mapEntry(data)
}

export async function updateDiaryEntry(id, updates) {
  const payload = { title: updates.title, content: updates.content, tags: updates.tags }
  const { data } = await API.patch(`/student/emotions/entries/${id}`, payload)
  return mapEntry(data)
}

export async function deleteDiaryEntry(id) {
  await API.delete(`/student/emotions/entries/${id}`)
}


