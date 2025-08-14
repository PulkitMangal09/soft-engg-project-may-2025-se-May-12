<template>
  <div class="min-h-screen bg-gray-50">
    <StudentNavBar />

    <div class="max-w-4xl mx-auto px-4 py-8">
      <!-- Header -->
      <div class="mb-8 text-center">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Join Connections</h1>
        <p class="text-lg text-gray-600">Connect with your teachers and family using invitation codes</p>
      </div>

      <!-- Connection Overview -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white rounded-xl shadow p-6 text-center">
          <span class="text-3xl mb-2">👨‍🏫</span>
          <div class="font-bold text-lg text-gray-800">{{ teacherConnections.length }}</div>
          <div class="text-sm text-gray-500">Teachers</div>
        </div>
        <!-- <div class="bg-white rounded-xl shadow p-6 text-center">
          <span class="text-3xl mb-2">👨‍👩‍👧‍👦</span>
          <div class="font-bold text-lg text-gray-800">{{ parentConnections.length }}</div>
          <div class="text-sm text-gray-500">Parents</div>
        </div> -->
        <div class="bg-white rounded-xl shadow p-6 text-center">
          <span class="text-3xl mb-2">👨‍👩‍👧‍👦</span>
          <div class="font-bold text-lg text-gray-800">{{ familyConnections.length }}</div>
          <div class="text-sm text-gray-500">Parents</div>
        </div>
      </div>

      <!-- Main Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Join Form -->
        <div class="bg-white rounded-xl shadow p-6">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Enter Invitation Code</h2>

          <form @submit.prevent="joinConnection" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Invitation Code</label>
              <input v-model.trim="invitationCode" type="text" placeholder="e.g., MATH-ABC123-XYZ789"
                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                required autocomplete="off">
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Relationship</label>
              <select v-model="relationship"
                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500">
                <option value="student">Student (to join a classroom)</option>
                <option value="child">Child (to join a family)</option>
                <option value="parent">Parent (rare for students, but supported)</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Message (Optional)</label>
              <textarea v-model="message" rows="3" placeholder="Add a short note for the approver…"
                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" />
            </div>

            <AppButton type="submit" label="Join Connection" icon="🔗" variant="primary" :loading="isSubmitting"
              class="w-full" />
          </form>

          <div class="mt-6 p-4 bg-blue-50 rounded-lg">
            <h4 class="font-semibold text-blue-800 mb-2">How it works</h4>
            <ul class="text-sm text-blue-700 space-y-1">
              <li>• Ask your teacher or parent for an invitation code</li>
              <li>• Enter the code and send your request</li>
              <li>• They’ll approve it, and you’ll be connected</li>
              <li>• Codes can expire or have limited uses</li>
            </ul>
          </div>
        </div>

        <!-- Your Connections -->
        <div class="bg-white rounded-xl shadow p-6">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Your Connections</h2>

          <div v-if="loading" class="text-center py-8 text-gray-500">Loading…</div>

          <template v-else>
            <div v-if="allConnections.length === 0" class="text-center py-8">
              <span class="text-4xl mb-4 block">🔗</span>
              <p class="text-gray-500">No connections yet. Enter an invitation code to get started!</p>
            </div>

            <div v-else class="space-y-6">
              <!-- Teachers -->
              <div v-if="teacherConnections.length">
                <h3 class="font-semibold text-gray-700 mb-3 flex items-center">
                  <span class="text-xl mr-2">👨‍🏫</span>
                  Teachers
                </h3>
                <div class="space-y-3">
                  <div v-for="t in teacherConnections" :key="t.connection_id || t.user_id_1 + '_' + t.user_id_2"
                    class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div class="flex items-center space-x-3">
                      <!-- <img :src="avatarFor(t)" class="h-10 w-10 rounded-full object-cover"> -->
                      <div>
                        <p class="font-semibold text-gray-800">{{ nameFor(t, 'Teacher') }}</p>
                        <p class="text-sm text-gray-500">teacher_student</p>
                      </div>
                    </div>
                    <AppBadge variant="success">Connected</AppBadge>
                  </div>
                </div>
              </div>

              <!-- Parents -->
              <div v-if="parentConnections.length">
                <h3 class="font-semibold text-gray-700 mb-3 flex items-center">
                  <span class="text-xl mr-2">👨‍👩‍👧‍👦</span>
                  Parents
                </h3>
                <div class="space-y-3">
                  <div v-for="p in parentConnections" :key="p.connection_id || p.user_id_1 + '_' + p.user_id_2"
                    class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div class="flex items-center space-x-3">
                      <!-- <img :src="avatarFor(p)" class="h-10 w-10 rounded-full object-cover"> -->
                      <div>
                        <p class="font-semibold text-gray-800">{{ nameFor(p, 'Parent') }}</p>
                        <p class="text-sm text-gray-500">{{ p.connection_type }}</p>
                      </div>
                    </div>
                    <AppBadge variant="success">Connected</AppBadge>
                  </div>
                </div>
              </div>

              <!-- Families -->
              <div v-if="familyConnections.length">
                <h3 class="font-semibold text-gray-700 mb-3 flex items-center">
                  <span class="text-xl mr-2">👨‍👩‍👧‍👦</span>
                  Parents
                </h3>
                <div class="space-y-3">
                  <div v-for="f in familyConnections" :key="f.connection_id || f.user_id_1 + '_' + f.user_id_2"
                    class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div class="flex items-center space-x-3">
                      <!-- <img :src="avatarFor(f)" class="h-10 w-10 rounded-full object-cover"> -->
                      <div>
                        <p class="font-semibold text-gray-800">{{ nameFor(f, 'Family') }}</p>
                        <p class="text-sm text-gray-500">family</p>
                      </div>
                    </div>
                    <AppBadge variant="success">Connected</AppBadge>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="mt-8 bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-bold text-gray-800">Recent Connection Activity</h2>
          <!-- CHANGED: secondary -> default -->
          <AppBadge variant="default">{{ recentActivity.length }} events</AppBadge>
        </div>

        <div v-if="activityLoading" class="text-center py-8 text-gray-500">Loading…</div>

        <div v-else class="space-y-3">
          <div v-for="a in recentActivity" :key="a.activity_id || a.timestamp"
            class="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
            <span class="text-lg">🔔</span>
            <div class="flex-1">
              <p class="text-sm text-gray-800">{{ a.message }}</p>
              <p class="text-xs text-gray-500">{{ a.timestamp ? new Date(a.timestamp).toLocaleString() : '' }}</p>
            </div>
            <!-- CHANGED: fallback 'secondary' -> 'default' -->
            <AppBadge :variant="a.status === 'success' ? 'success' : (a.status === 'warning' ? 'warning' : 'default')">
              {{ a.status || 'info' }}
            </AppBadge>
          </div>

          <div v-if="!recentActivity.length" class="text-center text-gray-500 py-6">
            No recent activity.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import axios from 'axios'
import StudentNavBar from '@/components/layout/StudentNavBar.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppBadge from '@/components/ui/AppBadge.vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export default {
  name: 'JoinConnectionView',
  components: { StudentNavBar, AppButton, AppBadge },
  setup() {
    const store = useStore()

    const invitationCode = ref('')
    const relationship = ref('student')
    const message = ref('')
    const isSubmitting = ref(false)

    const loading = ref(true)
    const activityLoading = ref(true)

    const teacherConnections = ref([])
    const parentConnections = ref([])
    const familyConnections = ref([])

    const recentActivity = ref([])

    const allConnections = computed(() => [
      ...teacherConnections.value,
      ...parentConnections.value,
      ...familyConnections.value
    ])

    const token = () => store.getters['auth/token']
    const authHeader = () => ({ headers: { Authorization: `Bearer ${token()}` } })

    const avatarFor = () =>
      `https://randomuser.me/api/portraits/${Math.random() > 0.5 ? 'women' : 'men'}/${Math.floor(Math.random() * 90) + 5}.jpg`
    const nameFor = (row, fallback) => row.partner_name || row.display_name || row.full_name || row.name || row.email || fallback

    async function fetchConnectionsByType(type) {
      const { data } = await axios.get(`${API_BASE_URL}/connections`, {
        ...authHeader(),
        params: { type }
      })
      if (Array.isArray(data)) return data
      if (Array.isArray(data?.connections)) return data.connections
      if (Array.isArray(data?.items)) return data.items
      return []
    }

    async function loadConnections() {
      try {
        loading.value = true
        if (!token()) throw new Error('Not authenticated')

        const [t, p, f] = await Promise.all([
          fetchConnectionsByType('teacher_student'),
          fetchConnectionsByType('parent_student'),
          fetchConnectionsByType('family')
        ])

        teacherConnections.value = t
        parentConnections.value = p
        familyConnections.value = f
      } catch (err) {
        console.error('Error loading connections:', err)
        store.dispatch('ui/showToast', {
          title: 'Error',
          message: err.response?.data?.detail || 'Failed to load connections',
          type: 'error'
        })
      } finally {
        loading.value = false
      }
    }

    async function loadActivity() {
      try {
        activityLoading.value = true
        if (!token()) return
        const { data } = await axios.get(`${API_BASE_URL}/connections/activity`, authHeader())
        recentActivity.value = Array.isArray(data?.activities) ? data.activities : []
      } catch (err) {
        console.error('Error loading activity:', err)
        recentActivity.value = []
      } finally {
        activityLoading.value = false
      }
    }

    async function joinConnection() {
      if (!invitationCode.value) return
      isSubmitting.value = true
      try {
        if (!token()) throw new Error('Not authenticated')

        await axios.post(
          `${API_BASE_URL}/requests/request`,
          {
            invitation_code: invitationCode.value.trim(),
            relationship: relationship.value,
            message: message.value || null
          },
          authHeader()
        )

        store.dispatch('ui/showToast', {
          title: 'Request sent!',
          message: 'Your connection request has been submitted.',
          type: 'success'
        })

        invitationCode.value = ''
        message.value = ''
        relationship.value = 'student'

        loadActivity()
        loadConnections()
      } catch (err) {
        console.error('Failed to redeem code:', err)
        store.dispatch('ui/showToast', {
          title: 'Failed',
          message: err.response?.data?.detail || 'Could not send the request',
          type: 'error'
        })
      } finally {
        isSubmitting.value = false
      }
    }

    onMounted(async () => {
      await Promise.all([loadConnections(), loadActivity()])
    })

    return {
      invitationCode,
      relationship,
      message,
      isSubmitting,
      loading,
      activityLoading,
      teacherConnections,
      parentConnections,
      familyConnections,
      recentActivity,
      allConnections,
      avatarFor,
      nameFor,
      joinConnection
    }
  }
}
</script>
