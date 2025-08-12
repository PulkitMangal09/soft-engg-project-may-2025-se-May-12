import axios from 'axios'
const API = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const asBearer = (t) => (typeof t === 'string' ? t : t?.access_token || t?.token || '')
const withAuth = (t) => ({ headers: { Authorization: `Bearer ${asBearer(t)}` } })

export const joinService = {
  // Join a family via Family Code (creates a pending join_request)
  async family({ family_code, role, message }, token) {
    const { data } = await axios.post(
      `${API}/parent/family/join`,
      { family_code, role, message },
      withAuth(token)
    )
    return data
  },

  // Join a classroom (teacher invite code). Creates a pending request teachers can approve.
  async classroom({ invite_code, relationship_type = 'parent_student', message }, token) {
    const { data } = await axios.post(
      `${API}/parent/classrooms/join`,
      { invite_code, relationship_type, message },
      withAuth(token)
    )
    return data
  },
}
