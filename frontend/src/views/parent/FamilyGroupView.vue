<template>
  <div class="bg-gray-100 font-sans p-4 md:p-6">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:justify-between md:items-center mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">👨‍👩‍👧‍👦 Smith Family Group</h1>
        <p class="text-sm text-gray-500">Family ID: SF_001234 • Created: January 2024</p>
      </div>
      <div class="mt-4 md:mt-0 flex space-x-3">
        <AppButton label="Generate Invitation Code" icon="🔑" variant="secondary" @click="isInvitationModalOpen = true" />
        <AppButton label="Edit Family" variant="secondary" size="sm" />
      </div>
    </div>

    <!-- Family Stats -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-white p-4 rounded-lg shadow-sm text-center">
        <p class="text-2xl font-bold text-blue-600">{{ familyMembers.length }}</p>
        <p class="text-xs text-gray-500">Total Members</p>
      </div>
      <div class="bg-white p-4 rounded-lg shadow-sm text-center">
        <p class="text-2xl font-bold text-amber-500">{{ joinRequests.length }}</p>
        <p class="text-xs text-gray-500">Pending Requests</p>
      </div>
      <div class="bg-white p-4 rounded-lg shadow-sm text-center">
        <p class="text-2xl font-bold text-green-600">{{ activeInvitations.length }}</p>
        <p class="text-xs text-gray-500">Active Codes</p>
      </div>
      <div class="bg-white p-4 rounded-lg shadow-sm text-center">
        <p class="text-2xl font-bold text-purple-600">{{ childrenCount }}</p>
        <p class="text-xs text-gray-500">Children</p>
      </div>
    </div>

    <!-- Active Invitation Codes -->
    <div class="mb-8">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold text-gray-700">🔑 Active Invitation Codes</h2>
        <AppButton label="Manage Codes" variant="secondary" size="sm" @click="isInvitationsModalOpen = true" />
      </div>
      <div v-if="activeInvitations.length === 0" class="bg-white rounded-lg shadow-sm p-6 text-center">
        <span class="text-4xl mb-4 block">🔑</span>
        <p class="text-gray-500 mb-4">No active invitation codes</p>
        <AppButton label="Generate First Code" variant="primary" @click="isInvitationModalOpen = true" />
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <AppCard v-for="invitation in activeInvitations.slice(0, 2)" :key="invitation.code">
          <div class="flex items-center justify-between mb-3">
            <code class="font-mono font-bold text-indigo-600 text-lg">{{ invitation.code }}</code>
            <AppBadge :variant="invitation.status === 'active' ? 'success' : 'warning'">
              {{ invitation.status }}
            </AppBadge>
          </div>
          <div class="space-y-2 text-sm text-gray-600">
            <p>Type: {{ invitation.type.replace('_', ' ') }}</p>
            <p>Uses: {{ invitation.uses }}/{{ invitation.maxUses }}</p>
            <p>Expires: {{ invitation.expiresAt }}</p>
          </div>
          <div class="flex space-x-2 mt-4">
            <AppButton label="Copy" size="sm" variant="secondary" @click="copyCode(invitation.code)" />
            <AppButton label="Revoke" size="sm" variant="error" @click="revokeCode(invitation.code)" />
          </div>
        </AppCard>
      </div>
    </div>

    <!-- Join Requests -->
    <div class="mb-8">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold text-gray-700">🔔 Join Requests ({{ joinRequests.length }})</h2>
        <router-link to="#" class="text-sm font-medium text-blue-600 hover:underline">View All</router-link>
      </div>
      <div v-if="joinRequests.length === 0" class="bg-white rounded-lg shadow-sm p-6 text-center">
        <span class="text-4xl mb-4 block">✅</span>
        <p class="text-gray-500">No pending join requests</p>
      </div>
      <div v-else class="space-y-4">
        <AppCard v-for="request in joinRequests" :key="request.id">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
            <div class="flex items-center mb-4 sm:mb-0">
              <img :src="request.avatar" class="w-12 h-12 rounded-full mr-4 object-cover">
              <div>
                <p class="font-bold text-gray-800">{{ request.name }}</p>
                <p class="text-sm text-gray-500">{{ request.relationship }} • {{ request.time }}</p>
                <p class="text-sm text-gray-500">{{ request.email }}</p>
              </div>
            </div>
            <div class="flex flex-col space-y-2">
                <p class="text-sm bg-gray-100 p-2 rounded-md italic">"{{ request.message }}"</p>
                <div class="flex space-x-2 justify-end">
                    <AppButton label="✓ Approve" variant="success" size="sm" @click="handleRequest(request.id, 'accepted')" />
                    <AppButton label="✗ Reject" variant="error" size="sm" @click="handleRequest(request.id, 'rejected')" />
                    <AppButton label="👁 Profile" variant="secondary" size="sm" />
                </div>
            </div>
          </div>
        </AppCard>
      </div>
    </div>

    <!-- Family Members -->
    <div>
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold text-gray-700">👥 Family Members ({{ familyMembers.length }})</h2>
        <router-link to="#" class="text-sm font-medium text-blue-600 hover:underline">Manage</router-link>
      </div>
      <div class="bg-white rounded-lg shadow-sm">
        <ul class="divide-y divide-gray-200">
          <li v-for="member in familyMembers" :key="member.id" class="p-4 flex justify-between items-center">
            <div class="flex items-center">
              <span class="text-2xl mr-4">{{ member.icon }}</span>
              <div>
                <p class="font-semibold text-gray-800">{{ member.name }}</p>
                <p class="text-sm text-gray-500">{{ member.role }} • {{ member.status }}</p>
                <p v-if="member.connectionType" class="text-xs text-blue-600">{{ member.connectionType }}</p>
              </div>
            </div>
            <div class="flex space-x-2">
                <AppButton v-for="action in member.actions" :key="action.label" :label="action.label" :variant="action.variant" size="sm" />
            </div>
          </li>
        </ul>
      </div>
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

    <!-- Manage Invitations Modal -->
    <AppModal :is-open="isInvitationsModalOpen" @close="isInvitationsModalOpen = false" title="Manage Invitation Codes">
      <div class="space-y-6">
        <div class="flex justify-between items-center">
          <h3 class="text-lg font-semibold">Active Invitation Codes</h3>
          <AppButton label="Generate New" variant="primary" size="sm" @click="isInvitationModalOpen = true" />
        </div>
        
        <div v-if="activeInvitations.length === 0" class="text-center py-8">
          <p class="text-gray-500">No active invitation codes.</p>
        </div>
        
        <div v-else class="space-y-4">
          <div v-for="invitation in activeInvitations" :key="invitation.code" 
               class="p-4 bg-gray-50 rounded-lg">
            <div class="flex items-center justify-between mb-3">
              <code class="font-mono font-bold text-indigo-600">{{ invitation.code }}</code>
              <AppBadge :variant="invitation.status === 'active' ? 'success' : 'warning'">
                {{ invitation.status }}
              </AppBadge>
            </div>
            <div class="grid grid-cols-2 gap-4 text-sm text-gray-600 mb-3">
              <div>
                <p><strong>Type:</strong> {{ invitation.type.replace('_', ' ') }}</p>
                <p><strong>Uses:</strong> {{ invitation.uses }}/{{ invitation.maxUses }}</p>
              </div>
              <div>
                <p><strong>Expires:</strong> {{ invitation.expiresAt }}</p>
                <p><strong>Created:</strong> {{ invitation.createdAt }}</p>
              </div>
            </div>
            <div class="flex space-x-2">
              <AppButton label="Copy" size="sm" variant="secondary" @click="copyCode(invitation.code)" />
              <AppButton label="Revoke" size="sm" variant="error" @click="revokeCode(invitation.code)" />
            </div>
          </div>
        </div>
      </div>
    </AppModal>

  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import AppCard from '@/components/ui/AppCard.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppModal from '@/components/ui/AppModal.vue'
import AppBadge from '@/components/ui/AppBadge.vue'

export default {
  name: 'FamilyGroupView',
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
    const isInvitationsModalOpen = ref(false)
    const generatedCode = ref('')
    
    const newInvitation = ref({
      type: 'parent_student',
      expiresIn: 24,
      maxUses: 1
    })

    const joinRequests = ref([
      {
        id: 1,
        name: 'Alex Johnson',
        relationship: 'Nephew',
        time: '2 hours ago',
        email: 'alex.johnson@email.com',
        message: 'Hi Uncle John, please add me to family group for school project',
        avatar: 'https://randomuser.me/api/portraits/men/32.jpg',
      },
      {
        id: 2,
        name: 'Maria Smith',
        relationship: 'Daughter',
        time: '1 day ago',
        email: 'maria.smith@email.com',
        message: 'Dad, I need to join for my financial literacy class',
        avatar: 'https://randomuser.me/api/portraits/women/44.jpg',
      },
    ])

    const familyMembers = ref([
      { 
        id: 1, 
        icon: '👨', 
        name: 'John Smith Sr. (You)', 
        role: 'Moderator', 
        status: 'Active', 
        connectionType: 'Family Head',
        actions: [{label: '👑', variant: 'secondary'}] 
      },
      { 
        id: 2, 
        icon: '👩', 
        name: 'Sarah Smith', 
        role: 'Moderator', 
        status: 'Active', 
        connectionType: 'Connected via invitation',
        actions: [{label: '💬', variant: 'secondary'}, {label: '⚙', variant: 'secondary'}] 
      },
      { 
        id: 3, 
        icon: '👦', 
        name: 'John Smith Jr.', 
        role: 'Child', 
        status: 'Last active: 2 hours ago', 
        connectionType: 'Connected via invitation',
        actions: [{label: '📊', variant: 'secondary'}, {label: '✉', variant: 'secondary'}] 
      },
      { 
        id: 4, 
        icon: '👧', 
        name: 'Emma Smith', 
        role: 'Child', 
        status: 'Last active: 30 minutes ago', 
        connectionType: 'Connected via invitation',
        actions: [{label: '🚨', variant: 'error'}, {label: '📊', variant: 'secondary'}] 
      },
      { 
        id: 5, 
        icon: '👶', 
        name: 'Sophie Smith', 
        role: 'Child', 
        status: 'Last active: 1 hour ago', 
        connectionType: 'Connected via invitation',
        actions: [{label: '📊', variant: 'secondary'}, {label: '✉', variant: 'secondary'}] 
      },
    ])

    const activeInvitations = ref([
      { 
        code: 'SMITH-FAM-ABC123', 
        type: 'parent_student', 
        status: 'active', 
        expiresAt: '2024-01-15', 
        uses: 0, 
        maxUses: 1,
        createdAt: '2024-01-10'
      },
      { 
        code: 'SMITH-FAM-XYZ789', 
        type: 'parent_parent', 
        status: 'active', 
        expiresAt: '2024-01-16', 
        uses: 1, 
        maxUses: 3,
        createdAt: '2024-01-11'
      },
    ])

    const childrenCount = computed(() => {
      return familyMembers.value.filter(member => member.role === 'Child').length
    })

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

    const handleRequest = (id, status) => {
      const request = joinRequests.value.find(req => req.id === id)
      if (!request) return

      joinRequests.value = joinRequests.value.filter(req => req.id !== id)

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
      joinRequests,
      familyMembers,
      activeInvitations,
      childrenCount,
      isInvitationModalOpen,
      isGeneratedCodeModalOpen,
      isInvitationsModalOpen,
      generatedCode,
      newInvitation,
      generateInvitationCode,
      copyToClipboard,
      copyCode,
      revokeCode,
      handleRequest,
    }
  },
}
</script>
