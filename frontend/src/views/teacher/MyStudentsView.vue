<template>
  <div class="p-6 md:p-8 bg-gray-100 min-h-screen">
    <!-- Header -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">My Students</h1>
        <div class="mt-1 flex items-center space-x-4">
          <div v-if="classrooms.length > 1" class="flex items-center space-x-2">
            <label class="text-sm font-medium text-gray-700">Classroom:</label>
            <select 
              v-model="selectedClassroom" 
              @change="loadClassroomStudents(selectedClassroom.classroom_id)"
              class="text-lg text-gray-600 bg-transparent border-none focus:ring-0 cursor-pointer"
            >
              <option v-for="classroom in classrooms" :key="classroom.classroom_id" :value="classroom">
                {{ classroom.name || `Classroom ${classroom.classroom_id}` }}
              </option>
            </select>
          </div>
          <p v-else-if="selectedClassroom" class="text-lg text-gray-600">
            {{ selectedClassroom.name || `Classroom ${selectedClassroom.classroom_id}` }}
          </p>
          <p v-else class="text-lg text-gray-600">Loading classrooms...</p>
        </div>
      </div>
      <div class="mt-4 md:mt-0 flex space-x-3">
        <AppButton label="Invite Students" icon="👥" variant="secondary" @click="isInviteModalOpen = true" />
        <AppButton label="Manage Invitations" icon="🔑" variant="secondary" @click="isInvitationsModalOpen = true" />
        <AppButton label="Add New Student" icon="👤" variant="primary" />
      </div>
    </div>

    <!-- Connection Stats -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <AppCard title="Connected Students">
        <p class="text-3xl font-bold text-indigo-600">{{ loading ? '...' : allStudents.length }}</p>
      </AppCard>
      <AppCard title="Active Invitations" variant="warning">
        <p class="text-3xl font-bold text-amber-500">{{ activeInvitations.length }}</p>
      </AppCard>
      <AppCard title="Pending Requests" variant="error">
        <p class="text-3xl font-bold text-red-500">{{ pendingRequests.length }}</p>
      </AppCard>
      <AppCard title="Total Classrooms" variant="success">
        <p class="text-3xl font-bold text-emerald-500">{{ loading ? '...' : classrooms.length }}</p>
      </AppCard>
    </div>

    <!-- Filter Tabs -->
    <div class="mb-6 flex space-x-2 border-b border-gray-200">
      <button v-for="tab in tabs" :key="tab.name"
        @click="activeTab = tab.name"
        :class="['px-4 py-2 text-sm font-medium rounded-t-lg transition-colors duration-200',
                 activeTab === tab.name ? 'bg-white text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700']">
        {{ tab.name }} ({{ tab.count }})
      </button>
    </div>

    <!-- Student Grid -->
    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-500 text-lg">Loading students...</p>
    </div>
    <div v-else-if="error" class="text-center py-12">
      <p class="text-red-500 text-lg">{{ error }}</p>
      <AppButton label="Retry" variant="primary" @click="loadAllData" class="mt-4" />
    </div>
    <div v-else-if="students.length === 0" class="text-center py-12">
      <p class="text-gray-500 text-lg">No students found for the selected filter.</p>
      <AppButton label="Invite Students" icon="👥" variant="primary" @click="isInviteModalOpen = true" class="mt-4" />
    </div>
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <AppCard v-for="student in students" :key="student.id" class="transform hover:-translate-y-1 transition-transform duration-200">
        <div class="flex flex-col items-center text-center">
          <div class="relative mb-4">
            <img class="h-24 w-24 rounded-full object-cover shadow-md" :src="student.avatar" :alt="student.name">
            <span class="absolute bottom-0 right-0 block h-6 w-6 rounded-full border-2 border-white"
                  :class="student.lastActive.includes('min') ? 'bg-green-400' : 'bg-gray-400'"></span>
          </div>
          <h3 class="text-lg font-bold text-gray-800">{{ student.name }}</h3>
          <p class="text-xs text-gray-500 mb-2">Last active: {{ student.lastActive }}</p>
          
          <AppBadge :variant="student.health.variant" class="mb-4">{{ student.health.text }}</AppBadge>

          <div class="w-full flex justify-around items-center border-t pt-3 mt-2 mb-3">
            <div class="text-center">
              <p class="text-xl font-bold text-indigo-600">{{ student.grade }}</p>
              <p class="text-xs text-gray-500">Grade</p>
            </div>
            <div class="text-center">
              <p class="text-xl font-bold text-indigo-600">{{ student.completion }}%</p>
              <p class="text-xs text-gray-500">Tasks</p>
            </div>
          </div>
          
          <!-- Student Actions -->
          <div class="w-full flex flex-col space-y-2">
            <AppButton 
              label="View Details" 
              size="sm" 
              variant="secondary" 
              class="w-full"
            />
            <div class="flex space-x-2">
              <AppButton 
                label="Remove" 
                size="sm" 
                variant="error" 
                class="flex-1"
                @click="removeStudentFromClass(student.student_id)"
                :disabled="!selectedClassroom"
              />
              <AppButton 
                label="Message" 
                size="sm" 
                variant="primary" 
                class="flex-1"
              />
            </div>
          </div>
        </div>
      </AppCard>
    </div>

    <!-- Invite Students Modal -->
    <AppModal :is-open="isInviteModalOpen" @close="isInviteModalOpen = false" title="Invite Students">
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
          <AppButton label="Cancel" variant="secondary" @click="isInviteModalOpen = false" />
          <AppButton label="Generate Code" variant="primary" @click="generateInvitationCode" />
        </div>
      </div>
    </AppModal>

    <!-- Manage Invitations Modal -->
    <AppModal :is-open="isInvitationsModalOpen" @close="isInvitationsModalOpen = false" title="Manage Invitation Codes">
      <div class="space-y-4">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold">Active Invitation Codes</h3>
          <AppButton label="Generate New" variant="primary" size="sm" @click="isInviteModalOpen = true" />
        </div>
        
        <div v-if="activeInvitations.length === 0" class="text-center py-8">
          <p class="text-gray-500">No active invitation codes.</p>
        </div>
        
        <div v-else class="space-y-3">
          <div v-for="invitation in activeInvitations" :key="invitation.code" class="p-4 bg-gray-50 rounded-lg">
            <div class="flex justify-between items-start">
              <div>
                <div class="flex items-center space-x-2 mb-2">
                  <code class="font-mono font-bold text-indigo-600">{{ invitation.code }}</code>
                  <AppBadge :variant="invitation.status === 'active' ? 'success' : 'warning'">
                    {{ invitation.status }}
                  </AppBadge>
                </div>
                <p class="text-sm text-gray-600">Type: {{ invitation.type.replace('_', ' ') }}</p>
                <p class="text-sm text-gray-600">Uses: {{ invitation.uses }}/{{ invitation.maxUses }}</p>
                <p class="text-sm text-gray-600">Expires: {{ invitation.expiresAt }}</p>
              </div>
              <div class="flex space-x-2">
                <AppButton label="Copy" size="sm" variant="secondary" @click="copyCode(invitation.code)" />
                <AppButton label="Revoke" size="sm" variant="error" @click="revokeCode(invitation.code)" />
              </div>
            </div>
          </div>
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
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import AppCard from '@/components/ui/AppCard.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import AppModal from '@/components/ui/AppModal.vue'
import { teacherService } from '@/services/teacherService.js'
import { invitationService } from '@/services/invitationService.js'

export default {
  name: 'MyStudentsView',
  components: { AppCard, AppButton, AppBadge, AppModal },
  setup() {
    const store = useStore()
    const activeTab = ref('All')
    const isInviteModalOpen = ref(false)
    const isInvitationsModalOpen = ref(false)
    const isGeneratedCodeModalOpen = ref(false)
    const generatedCode = ref('')
    const selectedClassroom = ref(null)
    
    // API data
    const classrooms = ref([])
    const allStudents = ref([])
    const studentsMetrics = ref([])
    const loading = ref(true)
    const error = ref(null)
    
    const newInvitation = ref({
      type: 'teacher_student',
      expiresIn: 24,
      maxUses: 1
    })

    // Computed properties for tabs and filtering
    const tabs = computed(() => {
      const needHelpCount = studentsMetrics.value.filter(s => s.tasks_overdue > 0).length
      const healthAlertsCount = studentsMetrics.value.filter(s => s.health_alerts > 0).length
      const topPerformersCount = studentsMetrics.value.filter(s => {
        const completionRate = s.tasks_assigned > 0 ? (s.tasks_completed / s.tasks_assigned) * 100 : 0
        return completionRate >= 90
      }).length
      
      return [
        { name: 'All', count: allStudents.value.length },
        { name: 'Need Help', count: needHelpCount },
        { name: 'Health Alerts', count: healthAlertsCount },
        { name: 'Top Performers', count: topPerformersCount },
      ]
    })

    // Filtered students based on active tab
    const students = computed(() => {
      let filtered = allStudents.value.map(student => {
        const metrics = studentsMetrics.value.find(m => m.student_id === student.student_id) || {
          tasks_assigned: 0,
          tasks_completed: 0,
          tasks_overdue: 0,
          health_alerts: 0
        }
        
        const completionRate = metrics.tasks_assigned > 0 
          ? Math.round((metrics.tasks_completed / metrics.tasks_assigned) * 100)
          : 0
        
        let grade = 'N/A'
        if (completionRate >= 90) grade = 'A'
        else if (completionRate >= 80) grade = 'B+'
        else if (completionRate >= 70) grade = 'B'
        else if (completionRate >= 60) grade = 'C+'
        else if (completionRate > 0) grade = 'C'
        
        return {
          id: student.student_id,
          student_id: student.student_id,
          name: student.full_name || `Student ${student.student_id}`,
          avatar: `https://randomuser.me/api/portraits/${Math.random() > 0.5 ? 'women' : 'men'}/${Math.floor(Math.random() * 99)}.jpg`,
          lastActive: '2 hours ago', // This would come from a real activity API
          health: {
            text: metrics.health_alerts > 0 ? `${metrics.health_alerts} health alert${metrics.health_alerts !== 1 ? 's' : ''}` : 'No health conditions',
            variant: metrics.health_alerts > 0 ? 'error' : 'default'
          },
          grade,
          completion: completionRate,
          grade_level: student.grade_level,
          ...metrics
        }
      })
      
      // Filter based on active tab
      switch (activeTab.value) {
        case 'Need Help':
          return filtered.filter(s => s.tasks_overdue > 0)
        case 'Health Alerts':
          return filtered.filter(s => s.health_alerts > 0)
        case 'Top Performers':
          return filtered.filter(s => s.completion >= 90)
        default:
          return filtered
      }
    })

    const activeInvitations = ref([])

    const pendingRequests = ref([
      { id: 1, name: 'Olivia Green', email: 'olivia.green@student.edu', requestedAt: '2 hours ago' },
      { id: 2, name: 'Ben Carter', email: 'ben.carter@student.edu', requestedAt: '1 day ago' },
    ])

    // Load data functions
    const loadClassrooms = async () => {
      try {
        const token = store.getters['auth/token']
        console.log('Token from store:', token ? 'Token exists' : 'No token found')
        if (!token) throw new Error('Please log in again to access student data')
        
        const data = await teacherService.getClassrooms(token)
        classrooms.value = data
        
        // If we have classrooms, select the first one by default
        if (data.length > 0 && !selectedClassroom.value) {
          selectedClassroom.value = data[0]
          await loadClassroomStudents(data[0].classroom_id)
        }
      } catch (err) {
        console.error('Error loading classrooms:', err)
        error.value = err.message
      }
    }
    
    const loadClassroomStudents = async (classroomId) => {
      try {
        const token = store.getters['auth/token']
        if (!token) throw new Error('No authentication token found')
        
        const data = await teacherService.getClassroomStudents(classroomId, token)
        allStudents.value = data
      } catch (err) {
        console.error('Error loading classroom students:', err)
        error.value = err.message
      }
    }
    
    const loadStudentsMetrics = async () => {
      try {
        const token = store.getters['auth/token']
        if (!token) throw new Error('No authentication token found')
        
        const data = await teacherService.getStudentsMetrics(token)
        studentsMetrics.value = data
      } catch (err) {
        console.error('Error loading student metrics:', err)
        error.value = err.message
      }
    }
    
    const loadAllData = async () => {
      try {
        loading.value = true
        error.value = null
        
        await Promise.all([
          loadClassrooms(),
          loadStudentsMetrics()
        ])
      } catch (err) {
        console.error('Error loading data:', err)
        store.dispatch('ui/showToast', {
          title: 'Error',
          message: 'Failed to load student data',
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
          status: 'active',
          expiresAt: code.expires_at ? new Date(code.expires_at).toLocaleDateString() : 'Never',
          uses: code.usage_count || 0,
          maxUses: code.max_uses || 'Unlimited',
          target_id: code.target_id
        }))
      } catch (err) {
        console.error('Error loading invitation codes:', err)
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
        const token = store.getters['auth/token']
        if (!token) {
          throw new Error('No authentication token found')
        }
        
        // Use the selected classroom or first available
        const targetClassroom = selectedClassroom.value || classrooms.value[0]
        
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
        
        isInviteModalOpen.value = false
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

    const copyCode = (code) => {
      navigator.clipboard.writeText(code)
      store.dispatch('ui/showToast', {
        title: 'Copied!',
        message: 'Invitation code copied to clipboard',
        type: 'success',
      })
    }

    const revokeCode = (code) => {
      activeInvitations.value = activeInvitations.value.filter(inv => inv.code !== code)
      store.dispatch('ui/showToast', {
        title: 'Code Revoked',
        message: 'Invitation code has been revoked',
        type: 'success',
      })
    }

    // Student management functions
    const addStudentToClass = async (studentId) => {
      if (!selectedClassroom.value) {
        store.dispatch('ui/showToast', {
          title: 'Error',
          message: 'No classroom selected',
          type: 'error',
        })
        return
      }

      try {
        const token = store.getters['auth/token']
        if (!token) throw new Error('No authentication token found')

        await teacherService.addStudentToClass(selectedClassroom.value.classroom_id, studentId, token)
        
        // Reload classroom students to reflect changes
        await loadClassroomStudents(selectedClassroom.value.classroom_id)
        
        store.dispatch('ui/showToast', {
          title: 'Success',
          message: 'Student added to classroom successfully',
          type: 'success',
        })
      } catch (err) {
        console.error('Error adding student to class:', err)
        store.dispatch('ui/showToast', {
          title: 'Error',
          message: 'Failed to add student to classroom',
          type: 'error',
        })
      }
    }

    const removeStudentFromClass = async (studentId) => {
      if (!selectedClassroom.value) {
        store.dispatch('ui/showToast', {
          title: 'Error',
          message: 'No classroom selected',
          type: 'error',
        })
        return
      }

      try {
        const token = store.getters['auth/token']
        if (!token) throw new Error('No authentication token found')

        await teacherService.removeStudentFromClass(selectedClassroom.value.classroom_id, studentId, token)
        
        // Reload classroom students to reflect changes
        await loadClassroomStudents(selectedClassroom.value.classroom_id)
        
        store.dispatch('ui/showToast', {
          title: 'Success',
          message: 'Student removed from classroom successfully',
          type: 'success',
        })
      } catch (err) {
        console.error('Error removing student from class:', err)
        store.dispatch('ui/showToast', {
          title: 'Error',
          message: 'Failed to remove student from classroom',
          type: 'error',
        })
      }
    }

    // Load data on mount
    onMounted(async () => {
      await loadAllData()
      await loadInvitationCodes()
    })
    
    return { 
      activeTab, 
      tabs, 
      students, 
      classrooms,
      selectedClassroom,
      allStudents,
      studentsMetrics,
      loading,
      error,
      isInviteModalOpen,
      isInvitationsModalOpen,
      isGeneratedCodeModalOpen,
      generatedCode,
      newInvitation,
      activeInvitations,
      pendingRequests,
      loadAllData,
      loadClassroomStudents,
      loadInvitationCodes,
      addStudentToClass,
      removeStudentFromClass,
      generateInvitationCode,
      copyToClipboard,
      copyCode,
      revokeCode
    }
  }
}
</script>
