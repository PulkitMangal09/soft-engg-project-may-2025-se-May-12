<template>
  <div class="min-h-screen bg-gray-50">
    <StudentNavBar />
    <div class="max-w-7xl mx-auto px-4 py-8">
      <!-- Header -->
      <div class="mb-8 text-center">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">My Connections</h1>
        <p class="text-lg text-gray-600">Manage your connections with teachers, parents, and families</p>
      </div>

      <!-- Connection Overview Stats -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-xl shadow p-6 text-center">
          <span class="text-3xl mb-2">👨‍🏫</span>
          <div class="font-bold text-lg text-gray-800">{{ teacherConnections.length }}</div>
          <div class="text-sm text-gray-500">Teachers</div>
        </div>
        <div class="bg-white rounded-xl shadow p-6 text-center">
          <span class="text-3xl mb-2">👨‍👩‍👧‍👦</span>
          <div class="font-bold text-lg text-gray-800">{{ parentConnections.length }}</div>
          <div class="text-sm text-gray-500">Parents</div>
        </div>
        <div class="bg-white rounded-xl shadow p-6 text-center">
          <span class="text-3xl mb-2">👥</span>
          <div class="font-bold text-lg text-gray-800">{{ familyConnections.length }}</div>
          <div class="text-sm text-gray-500">Families</div>
        </div>
        <div class="bg-white rounded-xl shadow p-6 text-center">
          <span class="text-3xl mb-2">⏳</span>
          <div class="font-bold text-lg text-gray-800">{{ pendingRequests.length }}</div>
          <div class="text-sm text-gray-500">Pending</div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="bg-white rounded-xl shadow p-6 mb-8">
        <h2 class="text-xl font-bold text-gray-800 mb-4">Quick Actions</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <AppButton label="Join New Connection" icon="🔗" variant="primary" @click="$router.push('/student/connections')" class="w-full" />
          <AppButton label="View All Tasks" icon="📝" variant="secondary" @click="$router.push('/student/tasks')" class="w-full" />
          <AppButton label="Chat Support" icon="💬" variant="secondary" @click="$router.push('/student/chat-support')" class="w-full" />
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Teacher Connections -->
        <div class="bg-white rounded-xl shadow p-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-xl font-bold text-gray-800 flex items-center">
              <span class="text-2xl mr-2">👨‍🏫</span>
              Teacher Connections
            </h2>
            <AppBadge variant="success">{{ teacherConnections.length }} Connected</AppBadge>
          </div>

          <div v-if="teacherConnections.length === 0" class="text-center py-8">
            <span class="text-4xl mb-4 block">📚</span>
            <p class="text-gray-500 mb-4">No teacher connections yet</p>
            <AppButton label="Join Teacher" variant="primary" @click="$router.push('/student/connections')" />
          </div>

          <div v-else class="space-y-4">
            <div v-for="teacher in teacherConnections" :key="teacher.id" class="p-4 bg-gray-50 rounded-lg">
              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center space-x-3">
                  <img :src="teacher.avatar" class="h-12 w-12 rounded-full object-cover">
                  <div>
                    <h3 class="font-semibold text-gray-800">{{ teacher.name }}</h3>
                    <p class="text-sm text-gray-500">{{ teacher.subject }}</p>
                  </div>
                </div>
                <AppBadge variant="success">Connected</AppBadge>
              </div>
              <div class="text-sm text-gray-600 mb-3">
                <p><strong>School:</strong> {{ teacher.school || '—' }}</p>
                <p><strong>Connected:</strong> {{ teacher.connectedAt }}</p>
                <p><strong>Active Tasks:</strong> {{ teacher.activeTasks }}</p>
              </div>
              <div class="flex space-x-2">
                <AppButton label="View Tasks" size="sm" variant="secondary" @click="viewTeacherTasks(teacher.id)" />
                <AppButton label="Chat" size="sm" variant="secondary" @click="chatWithTeacher(teacher.id)" />
                <AppButton label="Profile" size="sm" variant="secondary" @click="viewTeacherProfile(teacher.id)" />
              </div>
            </div>
          </div>
        </div>

        <!-- Parent Connections -->
        <div class="bg-white rounded-xl shadow p-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-xl font-bold text-gray-800 flex items-center">
              <span class="text-2xl mr-2">👨‍👩‍👧‍👦</span>
              Parent Connections
            </h2>
            <AppBadge variant="success">{{ parentConnections.length }} Connected</AppBadge>
          </div>

          <div v-if="parentConnections.length === 0" class="text-center py-8">
            <span class="text-4xl mb-4 block">🏠</span>
            <p class="text-gray-500 mb-4">No parent connections yet</p>
            <AppButton label="Join Family" variant="primary" @click="$router.push('/student/connections')" />
          </div>

          <div v-else class="space-y-4">
            <div v-for="parent in parentConnections" :key="parent.id" class="p-4 bg-gray-50 rounded-lg">
              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center space-x-3">
                  <img :src="parent.avatar" class="h-12 w-12 rounded-full object-cover">
                  <div>
                    <h3 class="font-semibold text-gray-800">{{ parent.name }}</h3>
                    <p class="text-sm text-gray-500">{{ parent.relationship }}</p>
                  </div>
                </div>
                <AppBadge variant="success">Connected</AppBadge>
              </div>
              <div class="text-sm text-gray-600 mb-3">
                <p><strong>Family:</strong> {{ parent.family || '—' }}</p>
                <p><strong>Connected:</strong> {{ parent.connectedAt }}</p>
                <p><strong>Data Access:</strong> {{ parent.dataAccess || '—' }}</p>
              </div>
              <div class="flex space-x-2">
                <AppButton label="Share Data" size="sm" variant="secondary" @click="manageDataSharing(parent.id)" />
                <AppButton label="Chat" size="sm" variant="secondary" @click="chatWithParent(parent.id)" />
                <AppButton label="Settings" size="sm" variant="secondary" @click="parentSettings(parent.id)" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Family Connections -->
      <div class="mt-8 bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-bold text-gray-800 flex items-center">
            <span class="text-2xl mr-2">👥</span>
            Family Groups
          </h2>
          <AppBadge variant="success">{{ familyConnections.length }} Connected</AppBadge>
        </div>

        <div v-if="familyConnections.length === 0" class="text-center py-8">
          <span class="text-4xl mb-4 block">🏘️</span>
          <p class="text-gray-500 mb-4">No family group connections yet</p>
          <AppButton label="Join Family Group" variant="primary" @click="$router.push('/student/connections')" />
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div v-for="family in familyConnections" :key="family.id" class="p-4 bg-gray-50 rounded-lg">
            <div class="flex items-center justify-between mb-3">
              <div>
                <h3 class="font-semibold text-gray-800">{{ family.name }}</h3>
                <p class="text-sm text-gray-500">{{ family.role }} • {{ family.memberCount }} members</p>
              </div>
              <AppBadge variant="success">Connected</AppBadge>
            </div>
            <div class="text-sm text-gray-600 mb-3">
              <p><strong>Head:</strong> {{ family.head || '—' }}</p>
              <p><strong>Joined:</strong> {{ family.joinedAt }}</p>
              <p><strong>Family Code:</strong> <code class="bg-gray-200 px-1 rounded">{{ family.code || '—' }}</code></p>
            </div>
            <div class="flex space-x-2">
              <AppButton label="View Family" size="sm" variant="secondary" @click="viewFamily(family.id)" />
              <AppButton label="Leave" size="sm" variant="error" @click="leaveFamily(family.id)" />
            </div>
          </div>
        </div>
      </div>

      <!-- Pending Requests -->
      <div v-if="pendingRequests.length > 0" class="mt-8 bg-white rounded-xl shadow p-6">
        <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <span class="text-2xl mr-2">⏳</span>
          Pending Connection Requests
        </h2>
        <div class="space-y-4">
          <div v-for="request in pendingRequests" :key="request.id" class="p-4 bg-amber-50 rounded-lg">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <img :src="request.avatar" class="h-10 w-10 rounded-full object-cover">
                <div>
                  <p class="font-semibold text-amber-800">{{ request.name }}</p>
                  <p class="text-sm text-amber-600">{{ request.type }} • {{ request.requestedAt }}</p>
                </div>
              </div>
              <AppBadge variant="warning">Pending</AppBadge>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="mt-8 bg-white rounded-xl shadow p-6">
        <h2 class="text-xl font-bold text-gray-800 mb-4">Recent Connection Activity</h2>
        <div class="space-y-3">
          <div v-for="activity in recentActivity" :key="activity.id" class="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
            <span class="text-lg">{{ activity.icon }}</span>
            <div class="flex-1">
              <p class="text-sm text-gray-800">{{ activity.message }}</p>
              <p class="text-xs text-gray-500">{{ activity.time }}</p>
            </div>
            <AppBadge :variant="activity.status === 'success' ? 'success' : 'warning'">{{ activity.status }}</AppBadge>
          </div>
        </div>
      </div>

      <!-- Privacy Settings -->
      <div class="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div class="bg-white rounded-xl shadow p-6">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Privacy & Settings</h2>
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <p class="font-semibold text-gray-800">Share Health Data</p>
                <p class="text-sm text-gray-500">Allow parents to view health metrics</p>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="privacySettings.healthData" class="sr-only peer">
                <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>
            <div class="flex items-center justify-between">
              <div>
                <p class="font-semibold text-gray-800">Share Academic Progress</p>
                <p class="text-sm text-gray-500">Allow teachers to view grades</p>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="privacySettings.academicData" class="sr-only peer">
                <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>
            <div class="flex items-center justify-between">
              <div>
                <p class="font-semibold text-gray-800">Share Financial Data</p>
                <p class="text-sm text-gray-500">Allow parents to view finances</p>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="privacySettings.financialData" class="sr-only peer">
                <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow p-6">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Connection Health</h2>
          <div class="space-y-4">
            <div class="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <div class="flex items-center space-x-3">
                <span class="text-2xl">✅</span>
                <div>
                  <p class="font-semibold text-green-800">All Connections Active</p>
                  <p class="text-sm text-green-600">Your connections are working properly</p>
                </div>
              </div>
            </div>
            <div class="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
              <div class="flex items-center space-x-3">
                <span class="text-2xl">📊</span>
                <div>
                  <p class="font-semibold text-blue-800">Data Sharing Active</p>
                  <p class="text-sm text-blue-600">Parents can view your progress</p>
                </div>
              </div>
            </div>
            <div class="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
              <div class="flex items-center space-x-3">
                <span class="text-2xl">🔔</span>
                <div>
                  <p class="font-semibold text-purple-800">Notifications Enabled</p>
                  <p class="text-sm text-purple-600">You'll be notified of updates</p>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import StudentNavBar from '@/components/layout/StudentNavBar.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import { connectionsService } from '@/services/connectionsService.js'

export default {
  name: 'StudentConnectionsView',
  components: { StudentNavBar, AppButton, AppBadge },
  setup() {
    const store = useStore()

    const teacherConnections = ref([])
    const parentConnections  = ref([])
    const familyConnections  = ref([])
    const pendingRequests    = ref([])
    const recentActivity     = ref([])
    const privacySettings    = ref({ healthData: true, academicData: true, financialData: false })

    const makeAvatar = () => `https://randomuser.me/api/portraits/${Math.random() > 0.5 ? 'women' : 'men'}/${Math.floor(Math.random()*90)+5}.jpg`
    const fmtDate = (iso) => iso ? new Date(iso).toLocaleDateString() : '—'

    async function loadConnections() {
      const teachers = await connectionsService.listConnections('teacher_student')
      const parents  = await connectionsService.listConnections('parent_student')
      const families = await connectionsService.listConnections('family')

      teacherConnections.value = (teachers || []).map((c) => ({
        id: c.connection_id || c.user_id_2 || c.user_id_1,
        name: c.partner_name || 'Teacher',
        subject: c.subject || '—',
        school: c.school || '—',
        avatar: makeAvatar(),
        connectedAt: fmtDate(c.established_at),
        activeTasks: c.active_tasks ?? 0,
      }))

      parentConnections.value = (parents || []).map((c) => ({
        id: c.connection_id || c.user_id_2 || c.user_id_1,
        name: c.partner_name || 'Parent',
        relationship: c.relationship || 'Parent',
        family: c.family_name || '—',
        dataAccess: c.data_access || '—',
        avatar: makeAvatar(),
        connectedAt: fmtDate(c.established_at),
      }))

      familyConnections.value = (families || []).map((c) => ({
        id: c.connection_id || c.family_id || c.user_id_2 || c.user_id_1,
        name: c.family_name || 'Family Group',
        role: c.role || 'Member',
        memberCount: c.member_count ?? 0,
        head: c.family_head || '—',
        joinedAt: fmtDate(c.established_at),
        code: c.family_code || null,
      }))
    }

    async function loadPending() {
      const mine = await connectionsService.getMyPendingRequests()
      pendingRequests.value = (mine || []).map((r) => ({
        id: r.request_id,
        name: r.requester_name || 'Request',
        type: r.target_type,
        avatar: makeAvatar(),
        requestedAt: fmtDate(r.created_at),
      }))
    }

    async function loadActivity() {
      const { activities } = await connectionsService.getActivity()
      recentActivity.value = (activities || []).map((a) => ({
        id: a.activity_id,
        icon: a.status === 'success' ? '✅' : '⏳',
        message: a.message,
        time: a.timestamp ? new Date(a.timestamp).toLocaleString() : '',
        status: a.status || 'pending',
      }))
    }

    // UI actions (stubs)
    const viewTeacherTasks   = (id) => store.dispatch('ui/showToast', { title: 'Viewing Tasks', message: 'Redirecting...', type: 'info' })
    const chatWithTeacher    = (id) => store.dispatch('ui/showToast', { title: 'Opening Chat', message: 'Starting chat...', type: 'info' })
    const viewTeacherProfile = (id) => store.dispatch('ui/showToast', { title: 'Teacher Profile', message: 'Opening profile...', type: 'info' })
    const manageDataSharing  = (id) => store.dispatch('ui/showToast', { title: 'Data Sharing', message: 'Opening settings...', type: 'info' })
    const chatWithParent     = (id) => store.dispatch('ui/showToast', { title: 'Opening Chat', message: 'Starting chat...', type: 'info' })
    const parentSettings     = (id) => store.dispatch('ui/showToast', { title: 'Parent Settings', message: 'Opening settings...', type: 'info' })
    const viewFamily         = (id) => store.dispatch('ui/showToast', { title: 'Family View', message: 'Opening family...', type: 'info' })
    const leaveFamily        = (id) => store.dispatch('ui/showToast', { title: 'Leave Family', message: 'Not implemented yet', type: 'warning' })

    onMounted(async () => {
      await Promise.all([loadConnections(), loadPending(), loadActivity()])
    })

    return {
      teacherConnections, parentConnections, familyConnections,
      pendingRequests, recentActivity, privacySettings,
      viewTeacherTasks, chatWithTeacher, viewTeacherProfile,
      manageDataSharing, chatWithParent, parentSettings,
      viewFamily, leaveFamily
    }
  }
}
</script>
D
