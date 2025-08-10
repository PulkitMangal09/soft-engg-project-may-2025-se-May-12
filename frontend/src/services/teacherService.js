import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

export const teacherService = {
  // GET /teacher/classrooms - List all classrooms owned by this teacher
  async getClassrooms(token) {
    try {
      const response = await axios.get(`${API_BASE_URL}/teacher/classrooms`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      return response.data
    } catch (error) {
      console.error('Error fetching classrooms:', error)
      throw error
    }
  },

  // GET /teacher/classrooms/{classroom_id}/students - List all students in a given classroom
  async getClassroomStudents(classroomId, token) {
    try {
      const response = await axios.get(`${API_BASE_URL}/teacher/classrooms/${classroomId}/students`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      return response.data
    } catch (error) {
      console.error('Error fetching classroom students:', error)
      throw error
    }
  },

  // POST /teacher/classrooms/{classroom_id}/students/{student_id} - Add student to class
  async addStudentToClass(classroomId, studentId, token) {
    try {
      const response = await axios.post(`${API_BASE_URL}/teacher/classrooms/${classroomId}/students/${studentId}`, {}, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      return response.data
    } catch (error) {
      console.error('Error adding student to class:', error)
      throw error
    }
  },

  // DELETE /teacher/classrooms/{classroom_id}/students/{student_id} - Remove student from class
  async removeStudentFromClass(classroomId, studentId, token) {
    try {
      const response = await axios.delete(`${API_BASE_URL}/teacher/classrooms/${classroomId}/students/${studentId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      return response.data
    } catch (error) {
      console.error('Error removing student from class:', error)
      throw error
    }
  }
}

// GET /teacher/students/metrics - Get student metrics across all classrooms
export const getStudentsMetrics = async (token) => {
  try {
    const response = await api.get('/teacher/students/metrics', {
      headers: { Authorization: `Bearer ${token}` }
    })
    return response.data
  } catch (error) {
    console.error('Error fetching student metrics:', error)
    throw error
  }
}

// Create a new classroom
export const createClassroom = async (classroomData, token) => {
  try {
    const response = await api.post('/teacher/classrooms', classroomData, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return response.data
  } catch (error) {
    console.error('Error creating classroom:', error)
    throw error
  }
}
