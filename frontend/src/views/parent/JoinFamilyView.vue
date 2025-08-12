<template>
  <div class="bg-gray-100 font-sans p-4 md:p-6">
    <!-- Header -->
    <div class="mb-8 text-center">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Join Family Groups</h1>
      <p class="text-lg text-gray-600">Connect with other families using invitation codes</p>
    </div>

    <!-- Connection Status -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow p-6 text-center">
        <span class="text-3xl mb-2">👨‍👩‍👧‍👦</span>
        <div class="font-bold text-lg text-gray-800">{{ familyConnections.length }}</div>
        <div class="text-sm text-gray-500">Family Groups</div>
      </div>
      <div class="bg-white rounded-xl shadow p-6 text-center">
        <span class="text-3xl mb-2">👥</span>
        <div class="font-bold text-lg text-gray-800">{{ totalMembers }}</div>
        <div class="text-sm text-gray-500">Total Members</div>
      </div>
      <div class="bg-white rounded-xl shadow p-6 text-center">
        <span class="text-3xl mb-2">⏳</span>
        <div class="font-bold text-lg text-gray-800">{{ pendingRequests.length }}</div>
        <div class="text-sm text-gray-500">Pending</div>
      </div>
      <div class="bg-white rounded-xl shadow p-6 text-center">
        <span class="text-3xl mb-2">🔗</span>
        <div class="font-bold text-lg text-gray-800">{{ activeConnections }}</div>
        <div class="text-sm text-gray-500">Active</div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Join Family Form -->
      <div class="bg-white rounded-xl shadow p-6">
        <h2 class="text-xl font-bold text-gray-800 mb-4">Enter Family Invitation Code</h2>
        <form @submit.prevent="joinFamily" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Family Invitation Code</label>
            <input 
              v-model="invitationCode" type="text" placeholder="e.g., FAM-ABC123-XYZ789"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" required
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Your Role in Family</label>
            <select v-model="selectedRole" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500">
              <option value="parent">Parent</option>
              <option value="guardian">Guardian</option>
              <option value="relative">Relative</option>
              <option value="friend">Family Friend</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Message (Optional)</label>
            <textarea v-model="message" rows="3" placeholder="Introduce yourself to the family..."
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            ></textarea>
          </div>
          <AppButton type="submit" label="Join Family" icon="🔗" variant="primary" :loading="isSubmitting" class="w-full" />
        </form>

        <div class="mt-6 p-4 bg-blue-50 rounded-lg">
          <h4 class="font-semibold text-blue-800 mb-2">How it works:</h4>
          <ul class="text-sm text-blue-700 space-y-1">
            <li>• Ask the family head for an invitation code</li>
            <li>• Enter the code above and send a request</li>
            <li>• The family head will review and approve your request</li>
            <li>• Once approved, you'll be connected to the family!</li>
          </ul>
        </div>
      </div>

      <!-- Current Family Connections -->
      <div class="bg-white rounded-xl shadow p-6">
        <h2 class="text-xl font-bold text-gray-800 mb-4">Your Family Connections</h2>

        <div v-if="familyConnections.length === 0" class="text-center py-8">
          <span class="text-4xl mb-4 block">👨‍👩‍👧‍👦</span>
          <p class="text-gray-500">No family connections yet. Enter an invitation code to get started!</p>
        </div>

        <div v-else class="space-y-4">
          <div v-for="family in familyConnections" :key="family.id" class="p-4 bg-gray-50 rounded-lg">
            <div class="flex items-center justify-between mb-3">
              <div>
                <h3 class="font-semibold text-gray-800">{{ family.name }}</h3>
                <p class="text-sm text-gray-500">{{ family.role }} • {{ family.memberCount }} members</p>
              </div>
              <AppBadge variant="success">Connected</AppBadge>
            </div>
            <div class="text-sm text-gray-600 mb-3">
              <p><strong>Head:</strong> {{ family.head }}</p>
              <p><strong>Joined:</strong> {{ family.joinedAt }}</p>
            </div>
            <div class="flex space-x-2">
              <AppButton label="View Family" size="sm" variant="secondary" />
              <AppButton label="Leave" size="sm" variant="error" @click="leaveFamily(family.id)" />
            </div>
          </div>
        </div>

        <!-- Pending Requests (local list just for UI) -->
        <div v-if="pendingRequests.length > 0" class="mt-6">
          <h3 class="font-semibold text-gray-700 mb-3 flex items-center">
            <span class="text-xl mr-2">⏳</span> Pending Requests
          </h3>
          <div class="space-y-3">
            <div v-for="request in pendingRequests" :key="request.id" class="p-3 bg-amber-50 rounded-lg">
              <div class="flex items-center justify-between">
                <div>
                  <p class="font-semibold text-amber-800">{{ request.familyName }}</p>
                  <p class="text-sm text-amber-600">{{ request.role }} • {{ request.requestedAt }}</p>
                </div>
                <AppBadge variant="warning">Pending</AppBadge>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="mt-8 bg-white rounded-xl shadow p-6">
      <h2 class="text-xl font-bold text-gray-800 mb-4">Recent Activity</h2>
      <div class="space-y-3">
        <div v-for="activity in recentActivity" :key="activity.id" class="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
          <span class="text-lg">{{ activity.icon }}</span>
          <div class="flex-1">
            <p class="text-sm text-gray-800">{{ activity.message }}</p>
            <p class="text-xs text-gray-500">{{ activity.time }}</p>
          </div>
          <AppBadge :variant="activity.status === 'success' ? 'success' : 'warning'">
            {{ activity.status }}
          </AppBadge>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import AppButton from '@/components/ui/AppButton.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import { familyGroupsService } from '@/services/familyGroupsService'  // provided earlier

export default {
  name: 'JoinFamilyView',
  components: { AppButton, AppBadge },
  setup() {
    const store = useStore()
    const token = () => store.getters['auth/token']

    // form
    const invitationCode = ref('')
    const selectedRole = ref('parent')
    const message = ref('')
    const isSubmitting = ref(false)

    // lists
    const familyConnections = ref([])
    const pendingRequests = ref([])
    const recentActivity = ref([])

    const loadConnections = async () => {
      try {
        const groups = await familyGroupsService.listGroups(token())
        familyConnections.value = (groups || []).map(g => ({
          id: g.family_id,
          name: g.family_name,
          role: 'Head',
          memberCount: Array.isArray(g.members) ? g.members.length : (g.member_count || 1),
          head: 'You',
          joinedAt: g.created_at ? new Date(g.created_at).toLocaleDateString() : '-'
        }))
      } catch {
        familyConnections.value = []
      }
    }

    const totalMembers = computed(() =>
      familyConnections.value.reduce((n, f) => n + (f.memberCount || 0), 0)
    )
    const activeConnections = computed(() => familyConnections.value.length)

    const joinFamily = async () => {
      if (!invitationCode.value.trim()) return
      isSubmitting.value = true
      try {
        await familyGroupsService.joinViaCode(
          {
            family_code: invitationCode.value.trim(),
            role: selectedRole.value,
            message: message.value?.trim() || null
          },
          token()
        )
        recentActivity.value.unshift({
          id: Date.now(),
          icon: '⏳',
          message: `Request sent with code ${invitationCode.value.trim()}`,
          time: 'Just now',
          status: 'pending'
        })
        store.dispatch('ui/showToast', {
          title: 'Request sent',
          message: 'The family head will review your request.',
          type: 'success'
        })
        invitationCode.value = ''
        selectedRole.value = 'parent'
        message.value = ''
      } catch (e) {
        const msg = e?.response?.data?.detail || 'Failed to send request'
        store.dispatch('ui/showToast', { title: 'Error', message: msg, type: 'error' })
      } finally {
        isSubmitting.value = false
      }
    }

    const leaveFamily = (familyId) => {
      store.dispatch('ui/showToast', { title: 'Not implemented', message: 'Leaving a family isn’t wired yet.', type: 'warning' })
    }

    onMounted(loadConnections)

    return {
      invitationCode, selectedRole, message, isSubmitting,
      familyConnections, pendingRequests, recentActivity,
      totalMembers, activeConnections,
      joinFamily, leaveFamily
    }
  }
}
</script>
