<template>
  <div class="p-6 md:p-8 bg-gray-100 min-h-screen">
    <!-- Header -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">My Students</h1>
        <p class="text-lg text-gray-600 mt-1">Grade 9A - Financial Literacy</p>
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
        <p class="text-3xl font-bold text-indigo-600">{{ students.length }}</p>
      </AppCard>
      <AppCard title="Active Invitations" variant="warning">
        <p class="text-3xl font-bold text-amber-500">{{ activeInvitations.length }}</p>
      </AppCard>
      <AppCard title="Pending Requests" variant="error">
        <p class="text-3xl font-bold text-red-500">{{ pendingRequests.length }}</p>
      </AppCard>
      <AppCard title="Connection Rate" variant="success">
        <p class="text-3xl font-bold text-emerald-500">85%</p>
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
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
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

          <div class="w-full flex justify-around items-center border-t pt-3 mt-2">
            <div class="text-center">
              <p class="text-xl font-bold text-indigo-600">{{ student.grade }}</p>
              <p class="text-xs text-gray-500">Grade</p>
            </div>
            <div class="text-center">
              <p class="text-xl font-bold text-indigo-600">{{ student.completion }}%</p>
              <p class="text-xs text-gray-500">Tasks</p>
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
import { ref } from 'vue'
import { useStore } from 'vuex'
import AppCard from '@/components/ui/AppCard.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import AppModal from '@/components/ui/AppModal.vue'

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
    
    const newInvitation = ref({
      type: 'teacher_student',
      expiresIn: 24,
      maxUses: 1
    })

    const tabs = ref([
      { name: 'All', count: 28 },
      { name: 'Need Help', count: 5 },
      { name: 'Health Alerts', count: 2 },
      { name: 'Top Performers', count: 4 },
    ])

    const students = ref([
      {
        id: 1, name: 'Emma Smith', avatar: 'https://randomuser.me/api/portraits/women/68.jpg', lastActive: '30 min ago',
        health: { text: 'Diabetes - High blood sugar', variant: 'error' }, grade: 'A', completion: 95
      },
      {
        id: 2, name: 'John Smith Jr.', avatar: 'https://randomuser.me/api/portraits/men/75.jpg', lastActive: '2 hours ago',
        health: { text: 'No health conditions', variant: 'default' }, grade: 'A-', completion: 88
      },
      {
        id: 3, name: 'Sarah Miller', avatar: 'https://randomuser.me/api/portraits/women/78.jpg', lastActive: '45 min ago',
        health: { text: 'No health conditions', variant: 'default' }, grade: 'A+', completion: 98
      },
      {
        id: 4, name: 'Michael Rodriguez', avatar: 'https://randomuser.me/api/portraits/men/32.jpg', lastActive: '1 day ago',
        health: { text: 'ADHD - Medication tracking', variant: 'warning' }, grade: 'C-', completion: 65
      },
      {
        id: 5, name: 'Lisa Chen', avatar: 'https://randomuser.me/api/portraits/women/44.jpg', lastActive: '3 hours ago',
        health: { text: 'No health conditions', variant: 'default' }, grade: 'B+', completion: 82
      },
      {
        id: 6, name: 'David Thompson', avatar: 'https://randomuser.me/api/portraits/men/11.jpg', lastActive: '6 hours ago',
        health: { text: 'No health conditions', variant: 'default' }, grade: 'B', completion: 79
      },
    ])

    const activeInvitations = ref([
      { code: 'MATH101-ABC123', type: 'teacher_student', status: 'active', expiresAt: '2024-01-15', uses: 0, maxUses: 1 },
      { code: 'MATH101-XYZ789', type: 'teacher_student', status: 'active', expiresAt: '2024-01-16', uses: 2, maxUses: 5 },
      { code: 'MATH101-DEF456', type: 'parent_student', status: 'active', expiresAt: '2024-01-17', uses: 1, maxUses: 3 },
    ])

    const pendingRequests = ref([
      { id: 1, name: 'Olivia Green', email: 'olivia.green@student.edu', requestedAt: '2 hours ago' },
      { id: 2, name: 'Ben Carter', email: 'ben.carter@student.edu', requestedAt: '1 day ago' },
    ])

    const generateInvitationCode = () => {
      // Generate a random code (in real app, this would call the API)
      const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
      let result = ''
      for (let i = 0; i < 8; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length))
      }
      generatedCode.value = `MATH101-${result}`
      
      isInviteModalOpen.value = false
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

    return { 
      activeTab, 
      tabs, 
      students, 
      isInviteModalOpen,
      isInvitationsModalOpen,
      isGeneratedCodeModalOpen,
      generatedCode,
      newInvitation,
      activeInvitations,
      pendingRequests,
      generateInvitationCode,
      copyToClipboard,
      copyCode,
      revokeCode
    }
  }
}
</script>
