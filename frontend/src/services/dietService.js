import axios from 'axios'

const API = axios

export async function getMeals() {
  const { data } = await API.get('/health/meals')
  return data || []
}

export async function logMeal(payload) {
  // payload: { mealtype, description, calories, proteins, carbs, fat }
  const { data } = await API.post('/health/meals', payload)
  return data
}
