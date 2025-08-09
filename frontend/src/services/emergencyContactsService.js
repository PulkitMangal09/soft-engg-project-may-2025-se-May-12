import axios from 'axios'

const API = axios

export async function listContacts() {
  const { data } = await API.get('/student/emotions/contacts')
  return data || []
}

export async function createContact(contact) {
  // contact: { name, phone_number, description?, contact_type, is_available_24_7? }
  const body = { ...contact }
  if (!body.description) delete body.description
  const { data } = await API.post('/student/emotions/contacts', body)
  return data
}

export async function updateContact(contactId, updates) {
  const body = { ...updates }
  if (body.description === '') body.description = null
  const { data } = await API.patch(`/student/emotions/contacts/${contactId}`, body)
  return data
}

export async function deleteContact(contactId) {
  await API.delete(`/student/emotions/contacts/${contactId}`)
}


