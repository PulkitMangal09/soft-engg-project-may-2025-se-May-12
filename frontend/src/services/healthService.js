import axios from 'axios'

export async function getLatestMetrics() {
  const res = await axios.get('/health/metrics')
  return res.data
}

export async function createMetrics(payload) {
  // payload: { weight, height, systolic, diastolic, blood_sugar, heart_rate, notes? }
  const res = await axios.post('/health/metrics', payload)
  return res.data
}
