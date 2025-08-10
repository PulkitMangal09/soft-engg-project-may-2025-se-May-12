import axios from 'axios'

const API = axios

// Conditions
export async function getConditions() {
  const { data } = await API.get('/medical/conditions')
  return data || []
}

export async function createCondition(payload) {
  const { data } = await API.post('/medical/conditions', payload)
  return data
}

export async function updateCondition(conditionId, payload) {
  const { data } = await API.patch(`/medical/conditions/${conditionId}`, payload)
  return data
}

export async function deleteCondition(conditionId) {
  const { data } = await API.delete(`/medical/conditions/${conditionId}`)
  return data
}

// Medications
export async function getMedications(params = {}) {
  const { conditionId } = params
  const url = conditionId ? `/medical/medications?condition_id=${conditionId}` : '/medical/medications'
  const { data } = await API.get(url)
  return data || []
}

export async function createMedication(payload) {
  const { data } = await API.post('/medical/medications', payload)
  return data
}

export async function updateMedication(medicationId, payload) {
  const { data } = await API.patch(`/medical/medications/${medicationId}`, payload)
  return data
}

export async function deleteMedication(medicationId) {
  const { data } = await API.delete(`/medical/medications/${medicationId}`)
  return data
}

// Medication Logs
export async function getMedicationLogs(medicationId) {
  const { data } = await API.get(`/medical/medications/${medicationId}/logs`)
  return data || []
}

export async function createMedicationLog(medicationId, payload) {
  const { data } = await API.post(`/medical/medications/${medicationId}/logs`, payload)
  return data
}
