import axios from 'axios'
const API = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const asBearer = (t) => (typeof t === 'string' ? t : t?.access_token || t?.token || '')
const withAuth = (t) => ({ headers: { Authorization: `Bearer ${asBearer(t)}` } })

export const parentReportsService = {
  async listStudents(token) {
    const { data } = await axios.get(`${API}/parent/reports/students`, withAuth(token))
    return data
  },
  async getStudentReport(token, studentId) {
    const { data } = await axios.get(`${API}/parent/reports/${studentId}`, withAuth(token))
    return data
  },
}
