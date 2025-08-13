<template>
  <div class="p-6 md:p-8 bg-gray-100 min-h-screen">
    <!-- Header -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Class Tasks</h1>
        <p class="text-lg text-gray-600 mt-1">Manage and track all class assignments.</p>
      </div>
      <!-- <button @click="showNewTask = true"
        class="mt-4 md:mt-0 inline-flex items-center px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700">
        📝 New Task
      </button> -->
    </div>

    <!-- Key Metrics -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow p-5">
        <p class="text-sm text-gray-500">Active Tasks</p>
        <p class="text-3xl font-bold text-indigo-600">{{ summary.activeTasks }}</p>
      </div>
      <div class="bg-white rounded-xl shadow p-5">
        <p class="text-sm text-gray-500">Overdue</p>
        <p class="text-3xl font-bold text-red-500">{{ summary.overdue }}</p>
      </div>
      <div class="bg-white rounded-xl shadow p-5">
        <p class="text-sm text-gray-500">Completion Rate</p>
        <p class="text-3xl font-bold text-emerald-500">{{ summary.completionRate }}</p>
      </div>
      <div class="bg-white rounded-xl shadow p-5">
        <p class="text-sm text-gray-500">Total This Month</p>
        <p class="text-3xl font-bold text-gray-800">{{ summary.totalThisMonth }}</p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Left Column: Recent Tasks -->
      <div class="lg:col-span-2 space-y-6">
        <div class="bg-white rounded-xl shadow p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold text-lg flex items-center gap-2">📋 Recent Tasks</h3>
            <button class="text-sm text-gray-500 hover:text-gray-700" @click="fetchRecent">Refresh</button>
          </div>

          <ul class="space-y-4" v-if="recent.length">
            <li v-for="(t, idx) in recent" :key="idx" class="p-4 border rounded-lg bg-white">
              <div class="flex justify-between items-start">
                <div>
                  <h4 class="font-bold text-gray-800">{{ t.title }}</h4>
                  <p class="text-sm text-gray-500">
                    Due: {{ t.due ? formatDate(t.due) : '—' }} • Assigned to: 1 student
                  </p>
                </div>
                <span class="text-xs px-2 py-1 rounded-full" :class="badgeClass(t.completed)">
                  {{ isItemComplete(t) ? 'Completed' : t.completed }}
                </span>
              </div>
              <div class="mt-3 h-2 bg-gray-200 rounded-full">
                <div class="h-2 rounded-full" :class="barClass(t.completed)"
                  :style="{ width: (isItemComplete(t) ? 100 : progressPercent(t.completed)) + '%' }"></div>
              </div>
            </li>
          </ul>
          <div v-else class="text-sm text-gray-500">No recent tasks.</div>
        </div>
      </div>

      <!-- Right Column: Overdue & Actions -->
      <div class="space-y-6">
        <div class="bg-white rounded-xl shadow p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold text-lg">⚠️ Overdue Tasks ({{ overdue.length }})</h3>
            <button class="text-sm text-gray-500 hover:text-gray-700" @click="fetchOverdue">Refresh</button>
          </div>
          <ul class="space-y-2" v-if="overdue.length">
            <li v-for="(t, i) in overdue" :key="i" class="text-sm text-gray-700">
              • <span class="font-medium">{{ t.title }}</span>
              <span class="text-gray-500">— due {{ t.due ? formatDate(t.due) : '—' }}</span>
            </li>
          </ul>
          <div v-else class="text-sm text-gray-500">No overdue tasks 🎉</div>

          <div class="mt-4 flex justify-end">
            <!-- <button class="px-3 py-2 rounded-lg bg-indigo-50 text-indigo-700 hover:bg-indigo-100">
              Send Reminders
            </button> -->
          </div>
        </div>

        <div class="bg-white rounded-xl shadow p-6">
          <h3 class="font-semibold text-lg mb-3">Actions</h3>
          <div class="grid grid-cols-1 gap-3">
            <button @click="showNewTask = true"
              class="px-3 py-2 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-800">
              📝 New Task
            </button>
            <button @click="goToReports" class="px-3 py-2 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-800">
              📊 Reports
            </button>
            <!-- <button class="px-3 py-2 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-800">
              📋 Templates
            </button> -->
          </div>
        </div>
      </div>
    </div>

    <!-- New Task Modal (reusable) -->
    <NewTaskModal :is-open="showNewTask" @close="showNewTask = false" @created="onTaskCreated" />
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useStore } from 'vuex'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
import NewTaskModal from '@/components/teacher/NewTaskModal.vue'

const store = useStore()
const router = useRouter()
const route = useRoute()

// ---- Token helpers: normalize and always include on requests ----
function getAuthHeader() {
  const stored = store.state?.auth?.token || localStorage.getItem('token') || ''
  if (!stored) return null
  // Normalize: remove any existing scheme and uppercase to "Bearer "
  const raw = stored.replace(/^bearer\s+/i, '').replace(/^Bearer\s+/, '')
  return `Bearer ${raw}`
}

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
})

API.interceptors.request.use(cfg => {
  const authHeader = getAuthHeader()
  if (authHeader) {
    cfg.headers.Authorization = authHeader
    // Debug once if needed:
    // console.log('[teacher] attaching auth:', authHeader.slice(0, 20) + '...')
  } else {
    // Optional: surface a toast if token missing
    // toast.error('You are not authenticated')
  }
  return cfg
})

function goToReports() {
  router.push('/teacher/reports')
}

// ---------------- UI state ----------------
const summary = ref({ activeTasks: 0, overdue: 0, completionRate: '0%', totalThisMonth: 0 })
const recent = ref([])
const overdue = ref([])

const showNewTask = ref(false)
const form = ref({
  title: '',
  description: '',
  category: '',
  priority: '',
  due_date: '',
  due_time: '',
  status: 'pending',
  reward_points: 0,
  attachment_url: '',
  assigned_to_email: ''
})

const categories = ['homework', 'project', 'study', 'personal', 'chore', 'health', 'financial']
const priorities = ['low', 'medium', 'high']

function formatDate(isoLike) {
  if (!isoLike) return '—'
  try {
    const d = new Date(isoLike)
    return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })
  } catch { return String(isoLike) }
}
function badgeClass(completedStr) {
  const [c, t] = completedStr.split('/').map(Number)
  const pct = t ? (c / t) * 100 : 0
  if (pct >= 80) return 'bg-emerald-100 text-emerald-700'
  if (pct >= 50) return 'bg-amber-100 text-amber-700'
  return 'bg-gray-100 text-gray-700'
}
function barClass(completedStr) {
  const [c, t] = completedStr.split('/').map(Number)
  const pct = t ? (c / t) * 100 : 0
  if (pct >= 80) return 'bg-emerald-500'
  if (pct >= 50) return 'bg-amber-500'
  return 'bg-indigo-500'
}
function progressPercent(completedStr) {
  const [c, t] = completedStr.split('/').map(Number)
  return t ? Math.min(100, Math.round((c / t) * 100)) : 0
}

function isComplete(completedStr) {
  return progressPercent(completedStr) === 100
}

function isItemComplete(item) {
  if (item && typeof item.is_completed === 'boolean') return item.is_completed
  return isComplete(item?.completed || '0/1')
}

// When a task is created from modal, refresh lists
function onTaskCreated() {
  fetchSummary(); fetchRecent(); fetchOverdue()
}

// ---------------- API calls ----------------
async function fetchSummary() {
  try {
    const { data } = await API.get('/teacher/tasks/summary')
    summary.value = data
  } catch (e) {
    toast.error(e.response?.data?.detail || 'Failed to load summary (401?)')
  }
}
async function fetchRecent() {
  try {
    const { data } = await API.get('/teacher/tasks/recent')
    recent.value = data
  } catch (e) {
    toast.error(e.response?.data?.detail || 'Failed to load recent tasks (401?)')
  }
}
async function fetchOverdue() {
  try {
    const { data } = await API.get('/teacher/tasks/overdue')
    overdue.value = data
  } catch (e) {
    toast.error(e.response?.data?.detail || 'Failed to load overdue tasks (401?)')
  }
}

async function createTask() {
  if (!form.value.title || !form.value.category || !form.value.priority || !form.value.assigned_to_email) {
    toast.error('Title, category, priority, and assigned_to_email are required')
    return
  }
  const payload = { ...form.value }

  if (payload.due_date) {
    const d = new Date(payload.due_date + 'T00:00:00')
    payload.due_date = d.toISOString()
  }
  if (!payload.due_time) delete payload.due_time
  if (!payload.attachment_url) delete payload.attachment_url
  if (!payload.description) delete payload.description
  // Ensure we do not accidentally send legacy field
  delete payload.assigned_to

  try {
    await API.post('/teacher/tasks/', payload)
    toast.success('Task created')
    showNewTask.value = false
    Object.assign(form.value, {
      title: '', description: '', category: '', priority: '',
      due_date: '', due_time: '', status: 'pending',
      reward_points: 0, attachment_url: '', assigned_to_email: ''
    })
    fetchSummary(); fetchRecent(); fetchOverdue()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Create failed')
  }
}

let _intervalId
onMounted(() => {
  // If store wasn’t hydrated yet, localStorage fallback in getAuthHeader() covers us
  const authHeader = getAuthHeader()
  if (!authHeader) {
    toast.error('Please log in')
    // Optionally redirect: window.location.href = '/login/teacher'
    return
  }
  // Open New Task modal if navigated with query flag
  if (route?.query?.newTask) {
    showNewTask.value = true
  }
  fetchSummary()
  fetchRecent()
  fetchOverdue()

  // Lightweight auto-refresh to reflect new completions
  _intervalId = setInterval(() => {
    fetchSummary()
    fetchRecent()
    fetchOverdue()
  }, 30000)
})

onUnmounted(() => {
  if (_intervalId) clearInterval(_intervalId)
})
</script>
