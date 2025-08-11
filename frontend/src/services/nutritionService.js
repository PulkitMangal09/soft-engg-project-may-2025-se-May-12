import axios from 'axios'

const API = axios

export async function generateSuggestions(range = 'today') {
  const { data } = await API.post(`/health/nutrition/suggestions/generate`, null, { params: { range } })
  return data
}

export async function getLatestSuggestions(range = 'today') {
  const { data } = await API.get(`/health/nutrition/suggestions/latest`, { params: { range } })
  return data
}

export async function listSuggestions(limit = 10) {
  const { data } = await API.get(`/health/nutrition/suggestions`, { params: { limit } })
  return data || []
}
