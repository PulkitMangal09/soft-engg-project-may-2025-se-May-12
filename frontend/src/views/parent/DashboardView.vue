<template>
  <div class="bg-gray-100 font-sans">
    <div class="p-4 md:p-6">
      <!-- Header -->
      <div class="mb-6 flex flex-col md:flex-row md:items-center md:justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-800">Smith Family Group</h1>
          <p class="text-sm text-gray-500">Moderator: John Smith Sr.</p>
        </div>
        <div class="mt-4 md:mt-0 flex space-x-3">
          <AppButton label="Generate Family Code" icon="🔑" variant="secondary" @click="isInvitationModalOpen = true" />
          <AppButton label="Manage Family" icon="👥" variant="primary" />
        </div>
      </div>

      <!-- Key Metrics -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6 text-center">
        <div class="bg-white p-3 rounded-lg shadow-sm">
          <p class="text-2xl font-bold text-blue-600">3</p>
          <p class="text-xs text-gray-500">Children</p>
        </div>
        <div class="bg-white p-3 rounded-lg shadow-sm">
          <p class="text-2xl font-bold text-amber-500">2</p>
          <p class="text-xs text-gray-500">Pending Requests</p>
        </div>
        <div class="bg-white p-3 rounded-lg shadow-sm">
          <p class="text-2xl font-bold text-green-600">15</p>
          <p class="text-xs text-gray-500">Active Tasks</p>
        </div>
        <div class="bg-white p-3 rounded-lg shadow-sm">
          <p class="text-2xl font-bold text-purple-600">{{ activeInvitations.length }}</p>
          <p class="text-xs text-gray-500">Active Codes</p>
        </div>
      </div>

      <!-- Children Selector -->
      <div class="flex items-center space-x-3 mb-6 overflow-x-auto pb-2">
        <button class="px-4 py-2 text-sm font-semibold text-white bg-blue-600 rounded-full shadow-md">All Children</button>
        <button v-for="child in children" :key="child.id" class="flex items-center space-x-2 px-4 py-2 text-sm font-semibold text-gray-700 bg-white rounded-full shadow-sm">
          <img :src="child.avatar" class="w-6 h-6 rounded-full object-cover">
          <span>{{ child.name }}</span>
        </button>
      </div>

      <!-- Urgent Alert -->
      <AppCard icon="🚨" title="Emma's blood sugar is elevated (180 mg/dL)" variant="error" class="mb-6">
        <p class="text-sm text-red-700">Immediate attention needed</p>
      </AppCard>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Attention Needed -->
        <AppCard title="⚠️ Attention Needed">
          <template #header-extra>
            <router-link to="/parent/tasks" class="text-sm font-medium text-blue-600 hover:underline">View All</router-link>
          </template>
          <ul class="space-y-3 text-sm text-gray-700">
            <li v-for="item in attentionItems" :key="item.text" class="flex items-start">
              <span class="mr-2">•</span>
              <span>{{ item.text }}</span>
            </li>
          </ul>
        </AppCard>

        <!-- Recent Achievements -->
        <AppCard title="✅ Recent Achievements">
          <template #header-extra>
            <AppButton label="Celebrate" size="sm" variant="secondary" />
          </template>
          <ul class="space-y-3 text-sm text-gray-700">
            <li v-for="item in achievements" :key="item.text">
              {{ item.text }}
            </li>
          </ul>
        </AppCard>
      </div>

      <!-- Family Connections Section -->
      <div class="mt-6">
        <AppCard title="👥 Family Connections" icon="🔗">
          <template #header-extra>
            <AppButton label="View All" size="sm" variant="secondary" @click="isConnectionsModalOpen = true" />
          </template>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="p-4 bg-blue-50 rounded-lg">
              <h4 class="font-semibold text-blue-800 mb-2">Active Invitation Codes</h4>
              <div v-if="activeInvitations.length === 0" class="text-sm text-blue-600">
                No active codes. Generate one to invite family members.
              </div>
              <div v-else class="space-y-2">
                <div v-for="invitation in activeInvitations.slice(0, 2)" :key="invitation.code" 
                     class="flex items-center justify-between text-sm">
                  <code class="font-mono text-blue-600">{{ invitation.code }}</code>
                  <span class="text-blue-500">{{ invitation.uses }}/{{ invitation.maxUses }}</span>
                </div>
              </div>
            </div>
            <div class="p-4 bg-amber-50 rounded-lg">
              <h4 class="font-semibold text-amber-800 mb-2">Pending Requests</h4>
              <div v-if="pendingRequests.length === 0" class="text-sm text-amber-600">
                No pending requests.
              </div>
              <div v-else class="space-y-2">
                <div v-for="request in pendingRequests.slice(0, 2)" :key="request.id" 
                     class="flex items-center justify-between text-sm">
                  <span class="text-amber-700">{{ request.name }}</span>
                  <span class="text-amber-500">{{ request.type }}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="mt-4 flex space-x-2">
            <AppButton label="Join Other Families" icon="🔗" variant="secondary" size="sm" @click="$router.push('/parent/join-family')" />
            <AppButton label="Manage Family" icon="👥" variant="secondary" size="sm" @click="$router.push('/parent/family')" />
          </div>
        </AppCard>
      </div>

      <!-- Quick Stats -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 text-center">
        <AppCard v-for="stat in quickStats" :key="stat.title" :icon="stat.icon" :title="stat.title" class="p-3">
          <p class="text-sm font-semibold text-gray-600">{{ stat.value }}</p>
        </AppCard>
      </div>

      <!-- Invitation Modal -->
      <AppModal :is-open="isInvitationModalOpen" @close="isInvitationModalOpen = false" title="Generate Family Invitation Code">
        <div class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Invitation Type</label>
            <select v-model="newInvitation.type" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500">
              <option value="parent_student">Child Invitation</option>
              <option value="parent_parent">Parent Invitation</option>
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
      <AppModal :is-open="isGeneratedCodeModalOpen" @close="isGeneratedCodeModalOpen = false" title="Family Invitation Code Generated">
        <div class="space-y-6">
          <div class="text-center">
            <div class="bg-gray-100 p-6 rounded-lg">
              <p class="text-sm text-gray-600 mb-2">Share this code with family members:</p>
              <div class="flex items-center justify-center space-x-2">
                <code class="text-2xl font-mono font-bold text-indigo-600 bg-white px-4 py-2 rounded border">{{ generatedCode }}</code>
                <AppButton label="Copy" icon="📋" size="sm" variant="secondary" @click="copyToClipboard" />
              </div>
            </div>
          </div>
          
          <div class="bg-blue-50 p-4 rounded-lg">
            <h4 class="font-semibold text-blue-800 mb-2">How to share:</h4>
            <ul class="text-sm text-blue-700 space-y-1">
              <li>• Share with your children or other parents</li>
              <li>• They enter this code in their app</li>
              <li>• You'll receive a join request to approve</li>
              <li>• Code expires in {{ newInvitation.expiresIn }} hours</li>
            </ul>
          </div>

          <div class="flex justify-end">
            <AppButton label="Done" variant="primary" @click="isGeneratedCodeModalOpen = false" />
          </div>
        </div>
      </AppModal>

      <!-- Connections Modal -->
      <AppModal :is-open="isConnectionsModalOpen" @close="isConnectionsModalOpen = false" title="Family Connections">
        <div class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Active Invitations -->
            <div>
              <h3 class="font-semibold text-gray-800 mb-3">Active Invitation Codes</h3>
              <div v-if="activeInvitations.length === 0" class="text-center py-4 text-gray-500">
                No active codes
              </div>
              <div v-else class="space-y-3">
                <div v-for="invitation in activeInvitations" :key="invitation.code" 
                     class="p-3 bg-gray-50 rounded-lg">
                  <div class="flex items-center justify-between mb-2">
                    <code class="font-mono font-bold text-indigo-600">{{ invitation.code }}</code>
                    <AppBadge variant="success">Active</AppBadge>
                  </div>
                  <p class="text-sm text-gray-600">Type: {{ invitation.type.replace('_', ' ') }}</p>
                  <p class="text-sm text-gray-600">Uses: {{ invitation.uses }}/{{ invitation.maxUses }}</p>
                  <p class="text-sm text-gray-600">Expires: {{ invitation.expiresAt }}</p>
                </div>
              </div>
            </div>

            <!-- Pending Requests -->
            <div>
              <h3 class="font-semibold text-gray-800 mb-3">Pending Requests</h3>
              <div v-if="pendingRequests.length === 0" class="text-center py-4 text-gray-500">
                No pending requests
              </div>
              <div v-else class="space-y-3">
                <div v-for="request in pendingRequests" :key="request.id" 
                     class="p-3 bg-amber-50 rounded-lg">
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-semibold text-amber-800">{{ request.name }}</span>
                    <AppBadge variant="warning">Pending</AppBadge>
                  </div>
                  <p class="text-sm text-amber-600">{{ request.type }}</p>
                  <p class="text-sm text-amber-600">Requested: {{ request.requestedAt }}</p>
                  <div class="flex space-x-2 mt-2">
                    <AppButton label="Accept" size="sm" variant="success" @click="handleRequest(request.id, 'accepted')" />
                    <AppButton label="Reject" size="sm" variant="error" @click="handleRequest(request.id, 'rejected')" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </AppModal>

    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'
import AppCard from '@/components/ui/AppCard.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppModal from '@/components/ui/AppModal.vue'
import AppBadge from '@/components/ui/AppBadge.vue'

export default {
  name: 'ParentDashboard',
  components: {
    AppCard,
    AppButton,
    AppModal,
    AppBadge,
  },
  setup() {
    const store = useStore()
    const isInvitationModalOpen = ref(false)
    const isGeneratedCodeModalOpen = ref(false)
    const isConnectionsModalOpen = ref(false)
    const generatedCode = ref('')
    
    const newInvitation = ref({
      type: 'parent_student',
      expiresIn: 24,
      maxUses: 1
    })

    const children = ref([
      { id: 1, name: 'John Jr.', avatar: 'https://randomuser.me/api/portraits/men/75.jpg' },
      { id: 2, name: 'Emma', avatar: 'https://randomuser.me/api/portraits/women/75.jpg' },
      { id: 3, name: 'Sophie', avatar: 'https://randomuser.me/api/portraits/women/76.jpg' },
    ])

    const attentionItems = ref([
      { text: 'John Jr.: Overdue math assignment' },
      { text: 'Emma: High sugar intake (3 days)' },
      { text: 'Sophie: Exceeded entertainment budget' },
    ])

    const achievements = ref([
      { text: 'John Jr.: Completed savings goal 🎮' },
      { text: 'Emma: 7-day water intake streak 💧' },
      { text: 'Sophie: Perfect task completion week ⭐' },
    ])

    const quickStats = ref([
        { icon: '📝', title: 'Tasks', value: '12 pending' },
        { icon: '💰', title: 'Finance', value: '2 goals active' },
        { icon: '🍎', title: 'Health', value: '1 alert' },
        { icon: '👥', title: 'Family', value: '2 requests' },
    ])

    const activeInvitations = ref([
      { code: 'SMITH-FAM-ABC123', type: 'parent_student', status: 'active', expiresAt: '2024-01-15', uses: 0, maxUses: 1 },
      { code: 'SMITH-FAM-XYZ789', type: 'parent_parent', status: 'active', expiresAt: '2024-01-16', uses: 1, maxUses: 3 },
    ])

    const pendingRequests = ref([
      { id: 1, name: 'Sarah Johnson', type: 'Parent', requestedAt: '2 hours ago' },
      { id: 2, name: 'Mike Wilson', type: 'Child', requestedAt: '1 day ago' },
    ])

    const generateInvitationCode = () => {
      // Generate a random code (in real app, this would call the API)
      const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
      let result = ''
      for (let i = 0; i < 8; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length))
      }
      generatedCode.value = `SMITH-FAM-${result}`
      
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
      const request = pendingRequests.value.find(req => req.id === id)
      if (!request) return

      pendingRequests.value = pendingRequests.value.filter(req => req.id !== id)

      if (status === 'accepted') {
        store.dispatch('ui/showToast', {
          title: 'Request Accepted',
          message: `${request.name} has been added to your family.`,
          type: 'success',
        })
      } else {
        store.dispatch('ui/showToast', {
          title: 'Request Rejected',
          message: `${request.name}'s request has been rejected.`,
          type: 'error',
        })
      }
    }

    return {
      children,
      attentionItems,
      achievements,
      quickStats,
      isInvitationModalOpen,
      isGeneratedCodeModalOpen,
      isConnectionsModalOpen,
      generatedCode,
      newInvitation,
      activeInvitations,
      pendingRequests,
      generateInvitationCode,
      copyToClipboard,
      handleRequest,
    }
  },
}
</script>