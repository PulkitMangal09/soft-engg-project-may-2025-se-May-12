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
        <AppCard icon="🎓" title="Class" subtitle="Grade 9A - Financial Literacy">
          <div class="text-right">
            <p class="text-3xl font-bold text-gray-800">28</p>
            <p class="text-sm text-gray-500">Students</p>
          </div>
        </AppCard>
        <AppCard icon="🔔" title="Health Alerts" variant="error">
           <div class="text-right">
            <p class="text-3xl font-bold text-red-500">2</p>
            <p class="text-sm text-gray-500">Urgent</p>
          </div>
        </AppCard>
        <AppCard icon="📝" title="Pending Tasks" variant="warning">
          <div class="text-right">
            <p class="text-3xl font-bold text-amber-500">15</p>
            <p class="text-sm text-gray-500">Awaiting Review</p>
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
            <p class="text-3xl font-bold text-emerald-500">B+</p>
            <p class="text-sm text-gray-500">Improving</p>
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
            <ul class="space-y-3">
              <li class="flex items-center justify-between">
                <div>
                  <p class="font-semibold text-gray-800">Michael R.</p>
                  <p class="text-sm text-gray-500">3 overdue assignments</p>
                </div>
                <AppButton label="View Student" size="sm" variant="secondary" />
              </li>
              <li class="flex items-center justify-between">
                <div>
                  <p class="font-semibold text-gray-800">Sophia T.</p>
                  <p class="text-sm text-gray-500">Falling behind in tasks</p>
                </div>
                <AppButton label="View Student" size="sm" variant="secondary" />
              </li>
               <li class="flex items-center justify-between">
                <div>
                  <p class="font-semibold text-gray-800">James L.</p>
                  <p class="text-sm text-gray-500">Low engagement this week</p>
                </div>
                <AppButton label="View Student" size="sm" variant="secondary" />
              </li>
            </ul>
             <template #footer>
              <div class="flex justify-end">
                <AppButton label="View All Students" variant="primary" />
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
    </div>
  </template>
  
  <script>
  // These components should be globally registered or imported locally
  import { ref } from 'vue'
import { useStore } from 'vuex'
import AppCard from '@/components/ui/AppCard.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppModal from '@/components/ui/AppModal.vue'
  
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
    const generatedCode = ref('')
    
    const newInvitation = ref({
      type: 'teacher_student',
      expiresIn: 24,
      maxUses: 1
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

    const activeInvitations = ref([
      { code: 'MATH101-ABC123', type: 'teacher_student', expiresAt: '2024-01-15', uses: 0, maxUses: 1 },
      { code: 'MATH101-XYZ789', type: 'teacher_student', expiresAt: '2024-01-16', uses: 2, maxUses: 5 },
    ])

    const generateInvitationCode = () => {
      // Generate a random code (in real app, this would call the API)
      const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
      let result = ''
      for (let i = 0; i < 8; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length))
      }
      generatedCode.value = `MATH101-${result}`
      
      isInvitationModalOpen.value = false
      isGeneratedCodeModalOpen.value = true
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

    return {
      isJoinRequestsModalOpen,
      isInvitationModalOpen,
      isGeneratedCodeModalOpen,
      generatedCode,
      newInvitation,
      pendingRequests,
      activeInvitations,
      generateInvitationCode,
      copyToClipboard,
      handleRequest,
    }
  },
  }
  </script>
  
  <style scoped>
  /* Scoped styles for the dashboard */
  </style>
  