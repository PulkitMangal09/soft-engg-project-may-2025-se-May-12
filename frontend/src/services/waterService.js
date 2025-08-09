import axios from 'axios'

const API = axios

export async function getWaterSummary() {
  const { data } = await API.get('/health/water/summary')
  return data || { total_ml: 0, glasses: 0 }
}

export async function addWater(amount_ml = 250, container_type = 'glass') {
  const { data } = await API.post('/health/water', { amount_ml, container_type })
  return data
}

export async function getWaterLogs() {
  const { data } = await API.get('/health/water/logs')
  return data || []
}


