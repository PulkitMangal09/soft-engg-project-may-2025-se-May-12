// /src/services/teacherService.js
import axios from 'axios'

const API_BASE_URL = import.meta.env?.VITE_API_BASE_URL || 'http://localhost:8000'
const api = axios.create({ baseURL: API_BASE_URL })

const withAuth = (token) => ({ headers: { Authorization: `Bearer ${token}` } })

// ---- classrooms ----
const getClassrooms = async (token) => {
  const { data } = await api.get('/teacher/classrooms', withAuth(token))
  return Array.isArray(data) ? data : []
}

const createClassroom = async (classroom, token) => {
  // map UI fields -> API schema
  const payload = {
    name: classroom.name?.trim(),
    subject: classroom.subject?.trim(),
    school_name: classroom.school_name ?? classroom.schoolName ?? '',
    grade_level: classroom.grade_level ?? classroom.gradeLevel ?? null,
    max_students: classroom.max_students ?? classroom.maxStudents ?? null,
  }
  const { data } = await api.post('/teacher/classrooms', payload, withAuth(token))
  return data
}

const updateClassroom = async (id, updates, token) => {
  const payload = {}
  if ('name' in updates) payload.name = updates.name
  if ('subject' in updates) payload.subject = updates.subject
  if ('school_name' in updates || 'schoolName' in updates)
    payload.school_name = updates.school_name ?? updates.schoolName
  if ('grade_level' in updates || 'gradeLevel' in updates)
    payload.grade_level = updates.grade_level ?? updates.gradeLevel
  if ('max_students' in updates || 'maxStudents' in updates)
    payload.max_students = updates.max_students ?? updates.maxStudents
  if ('is_active' in updates || 'isActive' in updates)
    payload.is_active = updates.is_active ?? updates.isActive

  const { data } = await api.patch(`/teacher/classrooms/${id}`, payload, withAuth(token))
  return data
}

const deleteClassroom = async (id, token, { hard = false } = {}) => {
  const { data } = await api.delete(`/teacher/classrooms/${id}`, {
    ...withAuth(token),
    params: { hard },
  })
  return data
}

const getClassroomStudents = async (classroomId, token) => {
  const { data } = await api.get(
    `/teacher/classrooms/${classroomId}/students`,
    withAuth(token)
  )
  return data
}

// ---- metrics ----
const getStudentsMetrics = async (token) => {
  const { data } = await api.get('/teacher/students/metrics', withAuth(token))
  return (
    data || {
      total_classrooms: 0,
      active_classrooms: 0,
      total_students: 0,
      by_grade_level: {},
    }
  )
}

// ---- exports ----
export {
  getClassrooms,
  createClassroom,
  updateClassroom,
  deleteClassroom,
  getClassroomStudents,
  getStudentsMetrics,
}

export const teacherService = {
  getClassrooms,
  createClassroom,
  updateClassroom,
  deleteClassroom,
  getClassroomStudents,
  getStudentsMetrics,
}

export default teacherService
