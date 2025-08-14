<template>
  <div class="p-6 md:p-8 bg-gray-100 min-h-screen">
    <div class="mb-8 flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Teacher's Dashboard</h1>
        <p class="text-gray-600 mt-1">Welcome back, {{ teacherName }}!</p>
      </div>
      <div class="flex gap-3 mt-4 md:mt-0">
        <AppButton label="Assign New Task" icon="➕" variant="primary" @click="showNewTask = true" />
        <AppButton label="Invite Students & Parents" icon="🔗" variant="secondary" @click="openInvite()" />
      </div>
    </div>

    <AppCard class="mb-10">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <h2 class="text-xl font-bold text-gray-900 mb-4">Student Overview</h2>
          <div class="flex items-center justify-between border-b pb-3 mb-3">
            <div class="flex items-center gap-3">
              <span class="text-2xl text-blue-500">🎓</span>
              <p class="font-semibold text-gray-800">Total Students</p>
            </div>
            <p class="text-3xl font-bold text-gray-800">{{ totalStudents }}</p>
          </div>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <span class="text-2xl text-purple-500">🏫</span>
              <p class="font-semibold text-gray-800">Total Classrooms</p>
            </div>
            <p class="text-3xl font-bold text-gray-800">{{ totalClassrooms }}</p>
          </div>
        </div>

        <div>
          <h2 class="text-xl font-bold text-gray-900 mb-4">Urgent Actions</h2>
          <div class="border rounded-lg p-4 bg-red-50 mb-3">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <span class="text-2xl text-red-500">🔔</span>
                <p class="font-semibold text-gray-800">Health Conditions</p>
              </div>
              <p class="text-3xl font-bold text-red-500">{{ healthConditionsCount }}</p>
            </div>
            <div class="mt-2 text-sm text-red-600">
              <p>Review and address urgent health conditions reported by students.</p>
            </div>
          </div>
          <div class="border rounded-lg p-4 bg-amber-50">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <span class="text-2xl text-amber-500">📝</span>
                <p class="font-semibold text-gray-800">Overdue Tasks</p>
              </div>
              <p class="text-3xl font-bold text-amber-500">{{ overdueCount }}</p>
            </div>
            <div class="mt-2 flex justify-between items-center">
              <p class="text-sm text-amber-600">Check on tasks that need attention.</p>
              <router-link to="/teacher/tasks">
                <AppButton label="View All Tasks" variant="link" size="sm" />
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </AppCard>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <AppCard title="Your Classrooms" :subtitle="`${classrooms.length} listed`">
          <template #default>
            <div v-if="loadingClassrooms" class="text-gray-500">Loading classrooms…</div>
            <div v-else-if="classrooms.length === 0" class="text-gray-500">No classrooms found.</div>
            <div v-else class="space-y-4">
<div
  v-for="c in classrooms"
  :key="c.classroom_id"
  class="p-4 rounded-md bg-white shadow-sm border hover:shadow-md transition-shadow duration-200"
>
  <div class="flex justify-between items-start">
    <div class="max-w-[70%]">
      <p class="text-lg font-semibold text-gray-900 break-words">
        {{ c.classroom_name || c.name || 'Untitled Classroom' }}
      </p>
      <p class="text-sm text-gray-600 mt-1">
        <span v-if="c.subject">Subject: {{ c.subject }}</span>
        <span v-if="c.subject && c.grade_level" class="mx-2">•</span>
        <span v-if="c.grade_level">Grade: {{ c.grade_level }}</span>
      </p>
    </div>
    <div class="flex items-center gap-4">
      <div
        class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
        :class="c.is_active ? 'bg-green-50 text-green-700' : 'bg-gray-100 text-gray-600'"
      >
        {{ c.is_active ? 'Active' : 'Inactive' }}
      </div>
      <AppButton
        label="Invite"
        size="sm"
        variant="link"
        @click="openInvite(c, 'teacher_student')"
      />
    </div>
  </div>
</div>

            </div>
          </template>
          <template #footer>
            <div class="flex justify-end">
              <router-link to="/teacher/students">
                <AppButton label="Manage All Classrooms" variant="primary" />
              </router-link>
            </div>
          </template>
        </AppCard>
      </div>

      <div>
        <AppCard title="Students by Grade">
          <template #default>
            <div v-if="loadingMetrics" class="text-gray-500">Loading metrics…</div>
            <div v-else>
              <div v-if="gradeBuckets.length === 0" class="text-gray-500">
                No grade data yet.
              </div>
              <div v-else class="space-y-2">
                <div v-for="row in gradeBuckets" :key="row.grade"
                  class="flex items-center justify-between border rounded-lg px-3 py-2">
                  <div class="font-medium text-gray-800">Grade {{ row.grade }}</div>
                  <div class="text-gray-600">{{ row.count }} students</div>
                </div>
              </div>
            </div>
          </template>
        </AppCard>
      </div>
    </div>

    <TeacherInviteModal :is-open="inviteOpen" :classrooms="classrooms" :default-type="inviteDefaults.type"
      :preselected-classroom-id="inviteDefaults.classroomId" @close="inviteOpen = false" />
    <NewTaskModal :is-open="showNewTask" @close="showNewTask = false" @created="onTaskCreated" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import AppCard from '@/components/ui/AppCard.vue'
import AppButton from '@/components/ui/AppButton.vue'
import TeacherInviteModal from '@/components/invitations/TeacherInviteModal.vue'
import { teacherService } from '@/services/teacherService'
import { requestsService } from '@/services/requestsService'
import NewTaskModal from '@/components/teacher/NewTaskModal.vue'

const store = useStore()
const router = useRouter()
const token = computed(() => store.getters['auth/token'] || store.state.auth?.token || '')

const teacherName = ref(
  store.getters['auth/user']?.full_name ||
  store.state.auth?.user?.full_name ||
  (store.state.auth?.user?.email ? store.state.auth.user.email.split('@')[0] : '') ||
  'Teacher'
)

const classrooms = ref([])
const studentsMetrics = ref({
  total_classrooms: 0,
  active_classrooms: 0,
  total_students: 0,
  by_grade_level: {}
})
const loadingClassrooms = ref(false)
const loadingMetrics = ref(false)
const overdueCount = ref(0)
const healthConditionsCount = ref(0)

const totalStudents = computed(() => studentsMetrics.value?.total_students ?? 0)
const totalClassrooms = computed(() => studentsMetrics.value?.total_classrooms ?? 0)

const gradeBuckets = computed(() => {
  const serverMap = studentsMetrics.value?.by_grade_level || {}
  const entries = Object.entries(serverMap)
  return entries
    .map(([grade, count]) => ({ grade, count }))
    .sort((a, b) => {
      const an = Number(a.grade), bn = Number(b.grade)
      if (!Number.isNaN(an) && !Number.isNaN(bn)) return an - bn
      return String(a.grade).localeCompare(String(b.grade))
    })
})

const loadData = async () => {
  try {
    loadingClassrooms.value = true
    loadingMetrics.value = true
    const [cls, metrics] = await Promise.all([
      token.value ? teacherService.getClassrooms(token.value) : [],
      token.value ? teacherService.getStudentsMetrics(token.value) : null,
    ])
    classrooms.value = Array.isArray(cls) ? cls : []
    studentsMetrics.value = metrics || { total_classrooms: 0, active_classrooms: 0, total_students: 0, by_grade_level: {} }

    const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
    const authHeader = token.value ? { Authorization: `Bearer ${token.value.replace(/^bearer\s+/i, '').replace(/^Bearer\s+/, '')}` } : {}
    
    try {
      const overdueResp = await axios.get(`${API_BASE}/teacher/tasks/overdue`, { headers: authHeader })
      overdueCount.value = Array.isArray(overdueResp.data) ? overdueResp.data.length : 0
    } catch {
      overdueCount.value = 0
    }
    
    try {
      const studentsResp = await axios.get(`${API_BASE}/teacher/reports/students`, { headers: authHeader })
      const students = Array.isArray(studentsResp.data) ? studentsResp.data : []
      if (students.length) {
        const sid = students[0]?.student_id || students[0]?.id || students[0]?.studentId
        if (sid) {
          const reportResp = await axios.get(`${API_BASE}/teacher/reports/${sid}`, { headers: authHeader })
          const conditions = reportResp.data?.healthSummary?.conditions
          healthConditionsCount.value = Array.isArray(conditions) ? conditions.length : 0
        } else {
          healthConditionsCount.value = 0
        }
      } else {
        healthConditionsCount.value = 0
      }
    } catch {
      healthConditionsCount.value = 0
    }
  } catch (e) {
    console.error('Dashboard load error:', e)
    classrooms.value = []
  } finally {
    loadingClassrooms.value = false
    loadingMetrics.value = false
  }
}

onMounted(loadData)

onMounted(async () => {
  if ((!store.getters['auth/user'] || !store.getters['auth/user']?.full_name) && token.value) {
    try {
      const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
      const { data } = await axios.get(`${API_BASE}/users/me`, { headers: { Authorization: `Bearer ${token.value}` } })
      teacherName.value = data?.full_name || (data?.email ? data.email.split('@')[0] : teacherName.value)
    } catch {}
  }
})

const inviteOpen = ref(false)
const inviteDefaults = ref({ type: 'teacher_student', classroomId: null })
const openInvite = (row = null, type = 'teacher_student') => {
  inviteDefaults.value = { type, classroomId: row?.classroom_id || classrooms.value?.[0]?.classroom_id || null }
  inviteOpen.value = true
}

const showNewTask = ref(false)
const onTaskCreated = () => {
  loadData()
}
</script>