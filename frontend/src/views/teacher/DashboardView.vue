<template>
    <div class="p-6 md:p-8 bg-gray-100 min-h-screen">
      <!-- Header -->
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Teacher's Dashboard</h1>
          <p class="text-lg text-gray-600 mt-1">Welcome back, Mrs. Johnson!</p>
        </div>
        <div class="mt-4 md:mt-0 flex space-x-3">
          <AppButton label="Generate Invitation Code" icon="🔗" variant="secondary" @click="isInvitationModalOpen = true" />
          <AppButton label="Assign New Task" icon="➕" variant="primary" />
        </div>
      </div>
  
      <!-- Key Metrics -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <AppCard icon="🎓" title="Total Students" :subtitle="classrooms.length > 0 ? `${classrooms.length} Classroom${classrooms.length !== 1 ? 's' : ''}` : 'Loading...'">
          <div class="text-right">
            <p class="text-3xl font-bold text-gray-800">{{ loading ? '...' : totalStudents }}</p>
            <p class="text-sm text-gray-500">Students</p>
          </div>
        </AppCard>
        <AppCard icon="🔔" title="Health Alerts" variant="error">
           <div class="text-right">
            <p class="text-3xl font-bold text-red-500">{{ loading ? '...' : healthAlerts }}</p>
            <p class="text-sm text-gray-500">Active</p>
          </div>
        </AppCard>
        <AppCard icon="📝" title="Overdue Tasks" variant="warning">
          <div class="text-right">
            <p class="text-3xl font-bold text-amber-500">{{ loading ? '...' : overdueCount }}</p>
            <p class="text-sm text-gray-500">Need Attention</p>
          </div>
          <template #footer>
            <div class="flex justify-end">
              <router-link to="/teacher/tasks">
                <AppButton label="View All Tasks" variant="secondary" size="sm" />
              </router-link>
            </div>
          </template>
        </AppCard>
         <AppCard icon="📊" title="Class Average" variant="success">
          <div class="text-right">
            <p class="text-3xl font-bold text-emerald-500">{{ loading ? '...' : classAverage }}</p>
            <p class="text-sm text-gray-500">Performance</p>
          </div>
        </AppCard>
      </div>
  
      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Left Column: Alerts and Students -->
        <div class="lg:col-span-2 space-y-8">
          <AppCard title="Urgent Health Alerts" icon="🚨" variant="error">
            <ul class="space-y-3">
              <li class="flex items-center justify-between">
                <div>
                  <p class="font-semibold text-gray-800">Emma S. - High Blood Sugar</p>
                  <p class="text-sm text-gray-500">185 mg/dL (30 min ago)</p>
                </div>
                <AppButton label="View Details" size="sm" variant="secondary" />
              </li>
               <li class="flex items-center justify-between">
                <div>
                  <p class="font-semibold text-gray-800">Leo M. - Asthma Action Plan</p>
                  <p class="text-sm text-gray-500">Reminder: Inhaler check needed</p>
                </div>
                <AppButton label="View Details" size="sm" variant="secondary" />
              </li>
            </ul>
          </AppCard>
  
          <AppCard title="Students Requiring Attention" icon="⚠️" variant="warning">
            <div v-if="loading" class="text-center py-4">
              <p class="text-gray-500">Loading student data...</p>
            </div>
            <div v-else-if="classrooms.length === 0" class="text-center py-8">
              <p class="text-gray-500 mb-4">No classrooms found. Please create a classroom first.</p>
              <button
                @click="openCreateClassroomModal"
                class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
              >
                Create Your First Classroom
              </button>
            </div>
            <div v-else-if="studentsNeedingAttention.length === 0" class="text-center py-4">
              <p class="text-gray-500">All students are doing well! 🎉</p>
            </div>
            <ul v-else class="space-y-3">
              <li v-for="student in studentsNeedingAttention" :key="student.student_id" class="flex items-center justify-between">
                <div>
                  <p class="font-semibold text-gray-800">Student ID: {{ student.student_id }}</p>
                  <div class="text-sm text-gray-500">
                    <span v-if="student.tasks_overdue > 0">{{ student.tasks_overdue }} overdue task{{ student.tasks_overdue !== 1 ? 's' : '' }}</span>
                    <span v-if="student.tasks_overdue > 0 && student.health_alerts > 0"> • </span>
                    <span v-if="student.health_alerts > 0">{{ student.health_alerts }} health alert{{ student.health_alerts !== 1 ? 's' : '' }}</span>
                  </div>
                </div>
                <AppButton label="View Student" size="sm" variant="secondary" />
              </li>
            </ul>
             <template #footer>
              <div class="flex justify-end">
                <router-link to="/teacher/students">
                  <AppButton label="View All Students" variant="primary" />
                </router-link>
              </div>
            </template>
          </AppCard>
        </div>
  
        <!-- Right Column: Achievements & Join Requests -->
        <div class="space-y-8">
          <AppCard title="Class Achievements" icon="✅" variant="success">
            <ul class="list-disc list-inside text-gray-700 space-y-2">
              <li>Sarah M.: Perfect task completion week</li>
              <li>David L.: Improved from C to A-</li>
              <li>Class: 90% attendance this week</li>
              <li>Overall: 15% improvement in grades</li>
            </ul>
            <template #footer>
              <div class="flex justify-end">
                  <AppButton label="Send Recognition" variant="secondary" />
              </div>
            </template>
          </AppCard>
  
          <AppCard title="Connection Requests" icon="📧" @click="isJoinRequestsModalOpen = true" class="cursor-pointer hover:bg-gray-50 transition">
           <div class="flex items-center justify-between">
              <p class="text-lg font-semibold text-gray-700">{{ pendingRequests.length }} pending requests</p>
              <AppButton label="Review Requests" variant="primary" />
           </div>
           <div class="mt-3 text-sm text-gray-500">
             <p>{{ activeInvitations.length }} active invitation codes</p>
           </div>
        </AppCard>

        <AppCard title="Quick Actions" icon="⚡">
          <div class="space-y-3">
            <AppButton label="Invite New Students" icon="👥" variant="secondary" @click="isInvitationModalOpen = true" />
            <AppButton label="View All Connections" icon="🔗" variant="secondary" />
            <AppButton label="Manage Invitation Codes" icon="🔑" variant="secondary" />
          </div>
        </AppCard>
        </div>
      </div>

      <!-- Invitation Code Modal -->
      <AppModal :is-open="isInvitationModalOpen" @close="isInvitationModalOpen = false" title="Generate Invitation Code">
        <div class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Invitation Type</label>
            <select v-model="newInvitation.type" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500">
              <option value="teacher_student">Student Invitation</option>
              <option value="parent_student">Parent Invitation</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Expires In</label>
            <select v-model="newInvitation.expiresIn" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500">
              <option value="24">24 hours</option>
              <option value="48">48 hours</option>
              <option value="168">1 week</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Max Uses</label>
            <input v-model="newInvitation.maxUses" type="number" min="1" max="100" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500" placeholder="1">
          </div>

          <div class="flex justify-end space-x-3">
            <AppButton label="Cancel" variant="secondary" @click="isInvitationModalOpen = false" />
            <AppButton label="Generate Code" variant="primary" @click="generateInvitationCode" />
          </div>
        </div>
      </AppModal>

      <!-- Generated Code Modal -->
      <AppModal :is-open="isGeneratedCodeModalOpen" @close="isGeneratedCodeModalOpen = false" title="Invitation Code Generated">
        <div class="space-y-6">
          <div class="text-center">
            <div class="bg-gray-100 p-6 rounded-lg">
              <p class="text-sm text-gray-600 mb-2">Share this code with students:</p>
              <div class="flex items-center justify-center space-x-2">
                <code class="text-2xl font-mono font-bold text-indigo-600 bg-white px-4 py-2 rounded border">{{ generatedCode }}</code>
                <AppButton label="Copy" icon="📋" size="sm" variant="secondary" @click="copyToClipboard" />
              </div>
            </div>
          </div>
          
          <div class="bg-blue-50 p-4 rounded-lg">
            <h4 class="font-semibold text-blue-800 mb-2">How to share:</h4>
            <ul class="text-sm text-blue-700 space-y-1">
              <li>• Share in your classroom or via email</li>
              <li>• Students enter this code in their app</li>
              <li>• You'll receive a connection request to approve</li>
              <li>• Code expires in {{ newInvitation.expiresIn }} hours</li>
            </ul>
          </div>

          <div class="flex justify-end">
            <AppButton label="Done" variant="primary" @click="isGeneratedCodeModalOpen = false" />
          </div>
        </div>
      </AppModal>

      <AppModal :is-open="isJoinRequestsModalOpen" @close="isJoinRequestsModalOpen = false" title="Connection Requests">
        <div class="space-y-4">
          <div v-if="pendingRequests.length === 0" class="text-center py-8">
            <p class="text-gray-500">No pending connection requests.</p>
          </div>
          
          <div v-else>
            <div v-for="request in pendingRequests" :key="request.id" class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div class="flex items-center space-x-4">
                <img :src="request.avatar" class="h-12 w-12 rounded-full object-cover">
                <div>
                  <p class="font-semibold text-gray-800">{{ request.name }}</p>
                  <p class="text-sm text-gray-500">{{ request.email }}</p>
                  <p class="text-xs text-gray-400">Requested {{ request.requestedAt }}</p>
                </div>
              </div>
              <div class="flex space-x-2">
                <AppButton label="Accept" variant="success" size="sm" @click="handleRequest(request.id, 'accepted')" />
                <AppButton label="Reject" variant="error" size="sm" @click="handleRequest(request.id, 'rejected')" />
              </div>
            </div>
          </div>
        </div>
      </AppModal>

      <!-- Create Classroom Modal -->
      <AppModal :is-open="isCreateClassroomModalOpen" @close="isCreateClassroomModalOpen = false" title="Create New Classroom">
        <form @submit.prevent="createNewClassroom" class="space-y-4">
          <div>
            <label for="className" class="block text-sm font-medium text-gray-700 mb-1">Classroom Name</label>
            <input
              id="className"
              v-model="newClassroom.name"
              type="text"
              required
              placeholder="e.g., Math Grade 5A"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          <div>
            <label for="classSubject" class="block text-sm font-medium text-gray-700 mb-1">Subject</label>
            <input
              id="classSubject"
              v-model="newClassroom.subject"
              type="text"
              required
              placeholder="e.g., Mathematics, Science, English"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          <div>
            <label for="gradeLevel" class="block text-sm font-medium text-gray-700 mb-1">Grade Level</label>
            <input
              id="gradeLevel"
              v-model="newClassroom.grade_level"
              type="text"
              placeholder="e.g., Grade 5, Year 8, Senior"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          <div>
            <label for="classDescription" class="block text-sm font-medium text-gray-700 mb-1">Description (Optional)</label>
            <textarea
              id="classDescription"
              v-model="newClassroom.description"
              rows="3"
              placeholder="Brief description of the classroom..."
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            ></textarea>
          </div>

          <div class="flex justify-end space-x-3 pt-4">
            <AppButton 
              label="Cancel" 
              variant="secondary" 
              @click="isCreateClassroomModalOpen = false"
              type="button"
            />
            <AppButton 
              label="Create Classroom" 
              variant="primary" 
              type="submit"
              :disabled="creatingClassroom"
            />
          </div>
        </form>
      </AppModal>
    </div>
</template>

<script>
// These components should be globally registered or imported locally
import { ref, onMounted, computed } from 'vue'
  import { useStore } from 'vuex'
  import AppCard from '@/components/ui/AppCard.vue'
  import AppButton from '@/components/ui/AppButton.vue'
  import AppModal from '@/components/ui/AppModal.vue'
  import { teacherService, createClassroom } from '@/services/teacherService.js'
import { invitationService } from '@/services/invitationService.js'

  export default {
    name: 'TeacherDashboard',
    components: {
      AppCard,
      AppButton,
      AppModal,
    },
    setup() {
      const store = useStore()
      const isJoinRequestsModalOpen = ref(false)
      const isInvitationModalOpen = ref(false)
      const isGeneratedCodeModalOpen = ref(false)
      const isCreateClassroomModalOpen = ref(false)
      const generatedCode = ref('')
      const creatingClassroom = ref(false)

      // Dashboard data
      const classrooms = ref([])
      const studentsMetrics = ref([])
      const loading = ref(true)
      const error = ref(null)
      const invitationLoading = ref(false)

      const newInvitation = ref({
        type: 'teacher_student',
        expiresIn: 24,
        maxUses: 1
      })

      const newClassroom = ref({
        name: '',
        subject: '',
        description: '',
        grade_level: ''
      })

    const pendingRequests = ref([
      { 
        id: 1, 
        name: 'Olivia Green', 
        email: 'olivia.green@student.edu',
        avatar: 'https://randomuser.me/api/portraits/women/33.jpg',
        requestedAt: '2 hours ago'
      },
      { 
        id: 2, 
        name: 'Ben Carter', 
        email: 'ben.carter@student.edu',
        avatar: 'https://randomuser.me/api/portraits/men/45.jpg',
        requestedAt: '1 day ago'
      },
      { 
        id: 3, 
        name: 'Chloe Davis', 
        email: 'chloe.davis@student.edu',
        avatar: 'https://randomuser.me/api/portraits/women/55.jpg',
        requestedAt: '3 days ago'
      },
    ])

    // Computed properties for dashboard metrics
    const totalStudents = computed(() => {
      return studentsMetrics.value.length
    })

    const healthAlerts = computed(() => {
      return studentsMetrics.value.filter(student => student.health_alerts > 0).length
    })

    const pendingTasks = computed(() => {
      return studentsMetrics.value.reduce((total, student) => {
        return total + (student.tasks_assigned - student.tasks_completed)
      }, 0)
    })

    const overdueCount = computed(() => {
      return studentsMetrics.value.reduce((total, student) => {
        return total + student.tasks_overdue
      }, 0)
    })

    const classAverage = computed(() => {
      if (studentsMetrics.value.length === 0) return 'N/A'
      const totalCompletion = studentsMetrics.value.reduce((total, student) => {
        const completionRate = student.tasks_assigned > 0 
          ? (student.tasks_completed / student.tasks_assigned) * 100 
          : 0
        return total + completionRate
      }, 0)
      const average = totalCompletion / studentsMetrics.value.length
      if (average >= 90) return 'A'
      if (average >= 80) return 'B+'
      if (average >= 70) return 'B'
      if (average >= 60) return 'C+'
      return 'C'
    })

    // Students requiring attention (overdue tasks or health alerts)
    const studentsNeedingAttention = computed(() => {
      return studentsMetrics.value.filter(student => 
        student.tasks_overdue > 0 || student.health_alerts > 0
      ).slice(0, 5) // Show top 5
    })

    const activeInvitations = ref([])

    // Load dashboard data
    const loadDashboardData = async () => {
      try {
        loading.value = true
        error.value = null

        const token = store.getters['auth/token']
        console.log('Token from store:', token ? 'Token exists' : 'No token found')
        
        if (!token) {
          console.error('Authentication token not found in store')
          throw new Error('Please log in again to access the dashboard')
        }

        // Load classrooms and student metrics in parallel
        const [classroomsData, metricsData] = await Promise.all([
          teacherService.getClassrooms(token),
          teacherService.getStudentsMetrics(token)
        ])

        classrooms.value = classroomsData
        studentsMetrics.value = metricsData

      } catch (err) {
        console.error('Error loading dashboard data:', err)
        error.value = err.message || 'Failed to load dashboard data'
        store.dispatch('ui/showToast', {
          title: 'Error',
          message: 'Failed to load dashboard data',
          type: 'error',
        })
      } finally {
        loading.value = false
      }
    }

    // Load invitation codes
    const loadInvitationCodes = async () => {
      try {
        const token = store.getters['auth/token']
        if (!token) return
        
        const codes = await invitationService.getMyInvitationCodes(token, 'classroom')
        activeInvitations.value = codes.map(code => ({
          code_id: code.code_id,
          code: code.code,
          type: 'classroom',
          expiresAt: code.expires_at ? new Date(code.expires_at).toLocaleDateString() : 'Never',
          uses: code.usage_count || 0,
          maxUses: code.max_uses || 'Unlimited',
          target_id: code.target_id
        }))
      } catch (err) {
        console.error('Error loading invitation codes:', err)
      }
    }

    // Classroom creation functions
    const openCreateClassroomModal = () => {
      isCreateClassroomModalOpen.value = true
      // Reset form
      newClassroom.value = {
        name: '',
        subject: '',
        description: '',
        grade_level: ''
      }
    }

    const createNewClassroom = async () => {
      try {
        creatingClassroom.value = true
        const token = store.getters['auth/token']
        
        if (!token) {
          throw new Error('Authentication token not found')
        }

        const classroomData = await createClassroom(newClassroom.value, token)
        
        // Add the new classroom to the list
        classrooms.value.push(classroomData)
        
        // Close modal and show success message
        isCreateClassroomModalOpen.value = false
        store.dispatch('ui/showToast', {
          title: 'Success',
          message: `Classroom "${newClassroom.value.name}" created successfully!`,
          type: 'success',
        })

        // Reload dashboard data to get updated metrics
        await loadDashboardData()
        
      } catch (err) {
        console.error('Error creating classroom:', err)
        store.dispatch('ui/showToast', {
          title: 'Error',
          message: err.message || 'Failed to create classroom',
          type: 'error',
        })
      } finally {
        creatingClassroom.value = false
      }
    }

    const generateInvitationCode = async () => {
      if (classrooms.value.length === 0) {
        store.dispatch('ui/showToast', {
          title: 'Error',
          message: 'No classrooms found. Please create a classroom first.',
          type: 'error',
        })
        return
      }
      
      try {
        invitationLoading.value = true
        const token = store.getters['auth/token']
        if (!token) {
          throw new Error('No authentication token found')
        }
        
        // Use the first classroom for now (could be enhanced to let teacher choose)
        const targetClassroom = classrooms.value[0]
        
        // Calculate expiration date based on user selection
        const expiresAt = new Date()
        expiresAt.setHours(expiresAt.getHours() + parseInt(newInvitation.value.expiresIn))
        
        const codeData = {
          target_type: 'classroom',
          target_id: targetClassroom.classroom_id,
          max_uses: newInvitation.value.maxUses || null,
          expires_at: expiresAt.toISOString()
        }
        
        const result = await invitationService.generateCode(codeData, token)
        generatedCode.value = result.code
        
        // Reload invitation codes to show the new one
        await loadInvitationCodes()
        
        isInvitationModalOpen.value = false
        isGeneratedCodeModalOpen.value = true
        
        store.dispatch('ui/showToast', {
          title: 'Success',
          message: 'Invitation code generated successfully!',
          type: 'success',
        })
      } catch (err) {
        console.error('Error generating invitation code:', err)
        store.dispatch('ui/showToast', {
          title: 'Error',
          message: err.response?.data?.detail || 'Failed to generate invitation code',
          type: 'error',
        })
      } finally {
        invitationLoading.value = false
      }
    }

    const copyToClipboard = () => {
      navigator.clipboard.writeText(generatedCode.value)
      store.dispatch('ui/showToast', {
        title: 'Copied!',
        message: 'Invitation code copied to clipboard',
        type: 'success',
      })
    }

    const handleRequest = (id, status) => {
      const student = pendingRequests.value.find(req => req.id === id)
      if (!student) return

      pendingRequests.value = pendingRequests.value.filter(req => req.id !== id)

      if (status === 'accepted') {
        store.dispatch('ui/showToast', {
          title: 'Request Accepted',
          message: `${student.name} has been added to your class.`,
          type: 'success',
        })
      } else {
        store.dispatch('ui/showToast', {
          title: 'Request Rejected',
          message: `${student.name}'s request has been rejected.`,
          type: 'error',
        })
      }

      if (pendingRequests.value.length === 0) {
        isJoinRequestsModalOpen.value = false
      }
    }

    // Load data on component mount
    onMounted(async () => {
      await loadDashboardData()
      await loadInvitationCodes()
    })

    return {
      isJoinRequestsModalOpen,
      isInvitationModalOpen,
      isGeneratedCodeModalOpen,
      isCreateClassroomModalOpen,
      generatedCode,
      creatingClassroom,
      newInvitation,
      newClassroom,
      pendingRequests,
      activeInvitations,
      classrooms,
      studentsMetrics,
      loading,
      error,
      totalStudents,
      healthAlerts,
      pendingTasks,
      overdueCount,
      classAverage,
      studentsNeedingAttention,
      loadDashboardData,
      loadInvitationCodes,
      invitationLoading,
      generateInvitationCode,
      openCreateClassroomModal,
      createNewClassroom,
      copyToClipboard,
      handleRequest,
      }
    },
  }
</script>

<style scoped>
/* Scoped styles for the dashboard */
</style>
  