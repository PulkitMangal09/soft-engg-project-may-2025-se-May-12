<template>
  <div class="bg-gray-100 font-sans">
    <div class="p-4 md:p-6">
      <!-- Header -->
      <div class="mb-6 flex flex-col md:flex-row md:items-center md:justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-800">Parent Dashboard</h1>
          <p class="text-sm text-gray-500">Overview of family, tasks, and requests</p>
        </div>
        <div class="mt-4 md:mt-0 flex space-x-3">
          <AppButton label="Generate Family Code" icon="🔑" variant="secondary" @click="isInvitationModalOpen = true" />
          <AppButton label="Manage Family" icon="👥" variant="primary" />
        </div>
      </div>

      <!-- Key Metrics -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6 text-center">
        <div class="bg-white p-3 rounded-lg shadow-sm">
          <p class="text-2xl font-bold text-blue-600">{{ totalChildren }}</p>
          <p class="text-xs text-gray-500">Children</p>
        </div>
        <div class="bg-white p-3 rounded-lg shadow-sm">
          <p class="text-2xl font-bold text-amber-500">{{ totalPendingRequests }}</p>
          <p class="text-xs text-gray-500">Pending Requests</p>
        </div>
        <div class="bg-white p-3 rounded-lg shadow-sm">
          <p class="text-2xl font-bold text-green-600">{{ dashboardData?.pending_tasks || 0 }}</p>
          <p class="text-xs text-gray-500">Active Tasks</p>
        </div>
        <div class="bg-white p-3 rounded-lg shadow-sm">
          <p class="text-2xl font-bold text-purple-600">{{ totalActiveInvitations }}</p>
          <p class="text-xs text-gray-500">Active Codes</p>
        </div>
      </div>

      <!-- Children Selector -->
      <div class="flex items-center space-x-3 mb-6 overflow-x-auto pb-2">
        <button class="px-4 py-2 text-sm font-semibold text-white bg-blue-600 rounded-full shadow-md">All
          Children</button>
        <button v-for="child in children" :key="child.user_id || child.id"
          class="flex items-center space-x-2 px-4 py-2 text-sm font-semibold text-gray-700 bg-white rounded-full shadow-sm">
          <div
            class="flex h-6 w-6 items-center justify-center rounded-full bg-indigo-100 text-indigo-700 text-xs font-bold">
            {{ (child.full_name || child.name || child.email || '').slice(0, 1).toUpperCase() }}
          </div>
          <span>{{ child.full_name || child.name || child.email }}</span>
        </button>
      </div>

      <!-- Quick Stats -->
      <!-- <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 text-center">
        <AppCard v-for="stat in quickStats" :key="stat.title" :icon="stat.icon" :title="stat.title" class="p-3">
          <p class="text-sm font-semibold text-gray-600">{{ stat.value }}</p>
        </AppCard>
      </div> -->

      <!-- Urgent Alert (from nutrition suggestions) -->
      <!-- <AppCard v-if="urgentAlert" icon="🚨" :title="urgentAlert.title" variant="error" class="mb-6">
        <p class="text-sm text-red-700">{{ urgentAlert.message }}</p>
      </AppCard> -->

      <!-- Main Content Grid -->
      <!-- <div class="grid grid-cols-1 md:grid-cols-2 gap-6"> -->
      <!-- Attention Needed -->
      <!-- <AppCard title="⚠️ Attention Needed">
          <template #header-extra>
            <router-link to="/parent/tasks" class="text-sm font-medium text-blue-600 hover:underline">View
              All</router-link>
          </template>
<ul class="space-y-3 text-sm text-gray-700">
  <li v-for="item in attentionItems" :key="item.text" class="flex items-start">
    <span class="mr-2">•</span>
    <span>{{ item.text }}</span>
  </li>
</ul>
</AppCard> -->

      <!-- Recent Achievements -->
      <!-- <AppCard title="✅ Recent Achievements">
          <template #header-extra>
            <AppButton label="Celebrate" size="sm" variant="secondary" />
          </template>
          <ul class="space-y-3 text-sm text-gray-700">
            <li v-for="item in achievements" :key="item.text">
              {{ item.text }}
            </li>
          </ul>
        </AppCard> -->
      <!-- </div> -->

      <!-- Family Connections Section -->
      <div class="mt-6">
        <AppCard title="👥 Family Connections" icon="🔗">
          <template #header-extra>
            <AppButton label="View All" size="sm" variant="secondary" @click="isConnectionsModalOpen = true" />
          </template>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Active Invitations -->
            <div>
              <h4 class="font-semibold text-gray-800 mb-3">Active Invitation Codes</h4>
              <div v-if="activeInvitations.length === 0" class="text-center py-4 text-gray-500">
                No active codes
              </div>
              <div v-else class="space-y-3">
                <div v-for="invitation in activeInvitations" :key="invitation.code" class="p-3 bg-gray-50 rounded-lg">
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
              <h4 class="font-semibold text-gray-800 mb-3">Pending Requests</h4>
              <div v-if="pendingRequests.length === 0" class="text-center py-4 text-gray-500">
                No pending requests
              </div>
              <div v-else class="space-y-3">
                <div v-for="request in pendingRequests" :key="request.id" class="p-3 bg-amber-50 rounded-lg">
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-semibold text-amber-800">{{ request.name }}</span>
                    <AppBadge variant="warning">Pending</AppBadge>
                  </div>
                  <p class="text-sm text-amber-600">{{ request.type }}</p>
                  <p class="text-sm text-amber-600">Requested: {{ request.requestedAt }}</p>
                  <div class="flex space-x-2 mt-2">
                    <AppButton label="Accept" size="sm" variant="success"
                      @click="handleRequest(request.id, 'accepted')" />
                    <AppButton label="Reject" size="sm" variant="error"
                      @click="handleRequest(request.id, 'rejected')" />
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="mt-4 flex space-x-2">
            <AppButton label="Join Other Families" icon="🔗" variant="secondary" size="sm"
              @click="$router.push('/parent/join-family')" />
            <AppButton label="Manage Family" icon="👥" variant="secondary" size="sm"
              @click="$router.push('/parent/family')" />
          </div>
        </AppCard>
      </div>

      <!-- Quick Stats -->
      <!-- <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 text-center">
        <AppCard v-for="stat in quickStats" :key="stat.title" :icon="stat.icon" :title="stat.title" class="p-3">
          <p class="text-sm font-semibold text-gray-600">{{ stat.value }}</p>
        </AppCard>
      </div> -->

      <!-- Invitation Modal -->
      <AppModal :is-open="isInvitationModalOpen" @close="isInvitationModalOpen = false"
        title="Generate Family Invitation Code">
        <div class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Invitation Type</label>
            <select v-model="newInvitation.type"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500">
              <option value="parent_student">Child Invitation</option>
              <option value="parent_parent">Parent Invitation</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Expires In</label>
            <select v-model="newInvitation.expiresIn"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500">
              <option value="24">24 hours</option>
              <option value="48">48 hours</option>
              <option value="168">1 week</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Max Uses</label>
            <input v-model="newInvitation.maxUses" type="number" min="1" max="100"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500" placeholder="1">
          </div>

          <div class="flex justify-end space-x-3">
            <AppButton label="Cancel" variant="secondary" @click="isInvitationModalOpen = false" />
            <AppButton label="Generate Code" variant="primary" @click="generateInvitationCode" />
          </div>
        </div>
      </AppModal>

      <!-- Generated Code Modal -->
      <AppModal :is-open="isGeneratedCodeModalOpen" @close="isGeneratedCodeModalOpen = false"
        title="Family Invitation Code Generated">
        <div class="space-y-6">
          <div class="text-center">
            <div class="bg-gray-100 p-6 rounded-lg">
              <p class="text-sm text-gray-600 mb-2">Share this code with family members:</p>
              <div class="flex items-center justify-center space-x-2">
                <code class="text-2xl font-mono font-bold text-indigo-600 bg-white px-4 py-2 rounded border">{{ generatedCode
                }}</code>
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
                <div v-for="invitation in activeInvitations" :key="invitation.code" class="p-3 bg-gray-50 rounded-lg">
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
                <div v-for="request in pendingRequests" :key="request.id" class="p-3 bg-amber-50 rounded-lg">
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-semibold text-amber-800">{{ request.name }}</span>
                    <AppBadge variant="warning">Pending</AppBadge>
                  </div>
                  <p class="text-sm text-amber-600">{{ request.type }}</p>
                  <p class="text-sm text-amber-600">Requested: {{ request.requestedAt }}</p>
                  <div class="flex space-x-2 mt-2">
                    <AppButton label="Accept" size="sm" variant="success"
                      @click="handleRequest(request.id, 'accepted')" />
                    <AppButton label="Reject" size="sm" variant="error"
                      @click="handleRequest(request.id, 'rejected')" />
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
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import AppCard from '@/components/ui/AppCard.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppModal from '@/components/ui/AppModal.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import { parentService } from '@/services/parentService.js'
import { parentReportsService } from '@/services/parentReportsService.js'
import { familyCodesService } from '@/services/familyCodesService'

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
    const loading = ref(true)
    const error = ref(null)
    const invitationLoading = ref(false)

    const newInvitation = ref({
      type: 'parent_student',
      expiresIn: 24,
      maxUses: 1
    })

    // Dashboard data - will be loaded from APIs
    const children = ref([])
    const attentionItems = ref([])
    const achievements = ref([])
    const quickStats = ref([])
    const activeInvitations = ref([])
    const pendingRequests = ref([])
    const dashboardData = ref(null)
    const familyGroups = ref([])
    const urgentAlert = ref(null)

    // Computed properties for dynamic stats
    const totalChildren = computed(() => children.value.length)
    const totalPendingRequests = computed(() => pendingRequests.value.length)
    const totalActiveInvitations = computed(() => activeInvitations.value.length)

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

        // Load parent dashboard data and children in parallel
        const [dashboardResponse, childrenResponse] = await Promise.all([
          parentService.getDashboard(token),
          parentService.getChildren(token)
        ])

        dashboardData.value = dashboardResponse
        children.value = childrenResponse

        // Fetch one student's nutrition suggestion to surface alerts/risks
        if (children.value && children.value.length) {
          const first = children.value[0]
          const studentId = first.user_id || first.id
          try {
            const report = await parentReportsService.getStudentReport(token, studentId)
            const suggestion = report?.nutrition_suggestion || {}
            const alerts = Array.isArray(suggestion.alerts) ? suggestion.alerts : []
            if (alerts.length) {
              const pick = alerts[Math.floor(Math.random() * alerts.length)]
              const title = (typeof pick === 'string') ? pick : (pick.title || pick.heading || 'Health Alert')
              const message = (typeof pick === 'string') ? 'Please review your child\'s nutrition updates.' : (pick.description || pick.note || 'Please review your child\'s nutrition updates.')
              urgentAlert.value = { title, message }
            } else {
              urgentAlert.value = null
            }

            // Attention Needed: show one risk
            const risks = Array.isArray(suggestion.risks) ? suggestion.risks : []
            if (risks.length) {
              const r = risks[0]
              const text = (typeof r === 'string') ? r : (r.title || r.name || r.description || 'Risk requires attention')
              // Prepend or replace with a single risk item
              attentionItems.value = [{ text }]
            }
          } catch (e) {
            console.warn('Failed fetching student report for alerts/risks:', e)
          }
        }

        // Update quick stats based on real data
        quickStats.value = [
          // { icon: '📝', title: 'Tasks', value: `${dashboardResponse.pending_tasks || 0} pending` },
          { icon: '💰', title: 'Finance', value: `${dashboardResponse.active_goals || 0} goals active` },
          { icon: '🍎', title: 'Health', value: `${dashboardResponse.health_alerts || 0} alert${dashboardResponse.health_alerts !== 1 ? 's' : ''}` },
          { icon: '👥', title: 'Family', value: `${totalPendingRequests.value} requests` },
        ]

        // Recent achievements: use most recent completed task if present
        const rc = dashboardResponse?.recent_completed_task || (Array.isArray(dashboardResponse?.completed_tasks) ? dashboardResponse.completed_tasks[0] : null)
        const rcText = rc ? (typeof rc === 'string' ? rc : (rc.title || rc.name || rc.task_title)) : null
        if (rcText) {
          achievements.value = [{ text: `Completed: ${rcText}` }]
        }

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
        const codes = await familyCodesService.list(token)
        activeInvitations.value = (codes || []).map(code => ({
          code_id: code.code_id,
          code: code.code,
          type: code.target_type,
          expiresAt: code.expires_at ? new Date(code.expires_at).toLocaleDateString() : 'Never',
          uses: code.usage_count || 0,
          maxUses: code.max_uses ?? 'Unlimited',
          target_id: code.target_id
        }))
      } catch (err) {
        console.error('Error loading invitation codes:', err)
      }
    }

    // Load pending requests
    const loadPendingRequests = async () => {
      try {
        const token = store.getters['auth/token']
        if (!token) return

        const requests = await parentService.getFamilyJoinRequests(token)
        pendingRequests.value = requests.map(request => ({
          id: request.request_id,
          name: request.requester_name || 'Unknown',
          type: request.requester_type || 'Unknown',
          requestedAt: request.created_at ? new Date(request.created_at).toLocaleDateString() : 'Unknown'
        }))
      } catch (err) {
        console.error('Error loading pending requests:', err)
      }
    }

    const generateInvitationCode = async () => {
      try {
        // pick a family group to attach the code to (first one for now)
        const targetId = familyGroups.value?.[0]?.family_id || familyGroups.value?.[0]?.id;

        if (!targetId) {
          store.dispatch('ui/showToast', {
            title: 'No family group',
            message: 'Create a family group first to generate codes.',
            type: 'error'
          });
          return;
        }

        const payload = {
          target_id: targetId,                                       // ← REQUIRED
          max_uses: parseInt(newInvitation.value.maxUses) || null,
          expires_in_hours: parseInt(newInvitation.value.expiresIn) || null,
        };

        const res = await familyCodesService.create(payload, store.getters['auth/token']);
        generatedCode.value = res.code;

        await loadInvitationCodes();

        isInvitationModalOpen.value = false;
        isGeneratedCodeModalOpen.value = true;

        store.dispatch('ui/showToast', { title: 'Success', message: 'Code generated', type: 'success' });
      } catch (e) {
        const msg = e?.response?.data?.detail || 'Failed to generate invitation code';
        console.error(e);
        store.dispatch('ui/showToast', { title: 'Error', message: msg, type: 'error' });
      }
    };



    const copyToClipboard = () => {
      navigator.clipboard.writeText(generatedCode.value)
      store.dispatch('ui/showToast', {
        title: 'Copied!',
        message: 'Invitation code copied to clipboard',
        type: 'success',
      })
    }

    const handleRequest = async (id, status) => {
      try {
        const token = store.getters['auth/token']
        if (!token) return

        const request = pendingRequests.value.find(req => req.id === id)
        if (!request) return

        const action = status === 'accepted' ? 'approve' : 'reject'
        await parentService.respondToFamilyJoinRequest(id, action, token)

        // Remove from local list
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

        // Refresh dashboard data
        await loadDashboardData()

      } catch (err) {
        console.error('Error handling request:', err)
        store.dispatch('ui/showToast', {
          title: 'Error',
          message: 'Failed to process request',
          type: 'error',
        })
      }
    }

    // Load family groups for invitation generation
    const loadFamilyGroups = async () => {
      try {
        const token = store.getters['auth/token']
        if (!token) return

        const groups = await parentService.getFamilyGroups(token)
        familyGroups.value = groups
      } catch (err) {
        console.error('Error loading family groups:', err)
        // If no family groups exist, we might need to create one or show a message
        familyGroups.value = [{ id: 'default', name: 'Default Family' }] // Fallback
      }
    }

    // Load data on component mount
    onMounted(async () => {
      await Promise.all([
        loadDashboardData(),
        loadInvitationCodes(),
        loadPendingRequests(),
        loadFamilyGroups()
      ])
    })

    return {
      children,
      attentionItems,
      achievements,
      quickStats,
      loading,
      error,
      invitationLoading,
      totalChildren,
      totalPendingRequests,
      totalActiveInvitations,
      isInvitationModalOpen,
      isGeneratedCodeModalOpen,
      isConnectionsModalOpen,
      generatedCode,
      newInvitation,
      activeInvitations,
      pendingRequests,
      dashboardData,
      familyGroups,
      loadDashboardData,
      loadInvitationCodes,
      loadPendingRequests,
      generateInvitationCode,
      copyToClipboard,
      handleRequest,
    }
  },
}
</script>