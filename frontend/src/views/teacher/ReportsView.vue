<template>
  <div class="p-6 md:p-8 bg-gray-100 min-h-screen">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Student Reports</h1>
      <AppButton v-if="selectedStudent" label="Select Another Student" icon="🔄" @click="selectedStudent = null"
        variant="secondary" />
    </div>

    <div v-if="!selectedStudent" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <h2 class="col-span-full text-xl font-semibold text-gray-700 mb-2">Select a student to view their report:
      </h2>
      <div v-if="loading" class="col-span-full text-gray-500">Loading students…</div>
      <div v-else-if="error" class="col-span-full text-red-600">{{ error }}</div>
      <div v-else-if="students.length === 0" class="col-span-full text-gray-500">No students found.</div>
      <div v-else v-for="student in students" :key="student.student_id" @click="selectStudent(student)"
        class="p-4 bg-white rounded-lg shadow-md flex items-center space-x-4 cursor-pointer hover:shadow-lg hover:-translate-y-1 transition-all">
        <div class="h-12 w-12 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-lg">
          {{ student.full_name ? student.full_name.charAt(0) : '?' }}
        </div>
        <div>
          <p class="font-bold text-gray-800">{{ student.full_name || 'Unnamed' }}</p>
          <p class="text-sm text-gray-500">ID: {{ student.student_number || '—' }} • Grade {{ student.grade_level ?? '—'
            }}</p>
        </div>
      </div>
    </div>

    <div v-else>
      <AppCard class="mb-8">
        <div class="flex flex-col md:flex-row items-start md:items-center justify-between">
          <div class="flex flex-col md:flex-row items-start md:items-center mb-4 md:mb-0">
            <div
              class="h-16 w-16 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-2xl mr-4 flex-shrink-0">
              {{ selectedStudent.full_name ? selectedStudent.full_name.charAt(0) : '?' }}
            </div>
            <div>
              <h2 class="text-2xl font-bold text-gray-800">{{ selectedStudent.full_name }}</h2>
              <p class="text-sm text-gray-500">
                Student ID: {{ report?.student_number || selectedStudent.student_number || '—' }}
                • Grade {{ report?.grade_level || selectedStudent.grade_level || '—' }}
              </p>
              <AppBadge v-if="report?.healthSummary?.latestNutrition" variant="warning" class="mt-2">
                {{ latestRiskLabel() || 'Nutrition suggestions' }}
              </AppBadge>
            </div>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-2 gap-4 text-center w-full md:w-auto">
            <div class="border-l border-gray-200 pl-4">
              <p class="text-3xl font-bold text-indigo-600">{{ report?.academicPerformance?.completionRate || 'N/A' }}
              </p>
              <p class="text-xs text-gray-500">Task Completion</p>
            </div>
            <div>
              <p class="text-3xl font-bold text-indigo-600">{{ report?.academicPerformance?.completedTasks }}/{{
                report?.academicPerformance?.totalTasks }}</p>
              <p class="text-xs text-gray-500">Tasks Done</p>
            </div>
          </div>
        </div>
      </AppCard>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 space-y-8">
<AppCard title="Health Summary" icon="🏥">
  <template #action>
    <AppButton v-if="report?.healthSummary?.latestNutrition" label="View Details" size="sm" variant="secondary"
      @click="openLatestSuggestion" />
  </template>

  <!-- Add padding inside the card -->
  <div class="p-4 space-y-4">
    <div>
      <p class="font-semibold text-gray-700">Active Conditions:</p>
      <ul class="list-disc list-inside text-gray-700 ml-4 mt-2">
        <li v-for="(c, idx) in (report?.healthSummary?.conditions || [])" :key="idx">
          {{ c.condition_name }} ({{ c.severity }})
        </li>
        <li v-if="!(report?.healthSummary?.conditions || []).length" class="text-gray-500">None</li>
      </ul>
    </div>
    <hr class="border-gray-200">
    <div v-if="report?.healthSummary?.latestNutrition">
      <p class="font-semibold text-gray-700">Latest Nutrition Suggestions:</p>
      <div class="mt-2 text-gray-700">
        <AppBadge class="mb-2">{{ latestRiskLabel() || 'Nutrition Suggestions' }}</AppBadge>
        <p class="text-sm text-gray-500">
          Generated on: {{ formatDateTime(report.healthSummary.latestNutrition.generated_at) }}
        </p>
      </div>
    </div>
    <div v-else class="text-gray-500">No recent nutrition suggestions.</div>
  </div>
</AppCard>


          <AppCard title="Academic Performance" icon="📈">
            <ul class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <li class="p-4 bg-gray-50 rounded-lg">
                <span class="font-bold text-gray-800 text-lg">Task Completion Rate</span>
                <p class="text-2xl font-bold text-indigo-600 mt-1">{{ report?.academicPerformance?.completionRate || 'N/A'
                  }}</p>
                <p class="text-sm text-gray-500">({{ report?.academicPerformance?.completedTasks }}/{{
                  report?.academicPerformance?.totalTasks }}) tasks completed</p>
              </li>
              <li class="p-4 bg-gray-50 rounded-lg">
                <span class="font-bold text-gray-800 text-lg">Improvement Trend</span>
                <p class="text-2xl font-bold text-indigo-600 mt-1">{{ report?.academicPerformance?.improvement || '—' }}
                </p>
                <p class="text-sm text-gray-500">Performance over recent tasks</p>
              </li>
            </ul>
          </AppCard>
        </div>
        <div class="space-y-8">
          <AppCard title="Recent Activity" icon="📋">
            <ul class="space-y-4" v-if="taskTaskEvents().length">
              <li v-for="(e, i) in taskTaskEvents()" :key="i" class="flex items-start text-sm p-2 bg-gray-50 rounded-lg">
                <span class="text-gray-500 w-28 flex-shrink-0">{{ formatDateTime(e.when) }}:</span>
                <span class="flex-1 font-medium">{{ e.what }}</span>
              </li>
            </ul>
            <div v-else class="text-gray-500 text-sm">No recent activity.</div>
          </AppCard>
          <AppCard title="Actions" icon="⚡️">
            <div class="grid grid-cols-1 gap-3">
              <a :href="telLink || undefined" target="_self" class="block w-full">
                <AppButton class="w-full" label="Call Parent" icon="📞" variant="primary" :disabled="!telLink" />
              </a>
              <AppButton class="w-full" label="Assign Task" icon="📝" variant="secondary" @click="showNewTask = true" />
            </div>
          </AppCard>
        </div>
      </div>
    </div>

    <div v-if="showSuggestionModal" class="fixed inset-0 z-50 flex items-center justify-center">
      <div class="absolute inset-0 bg-black bg-opacity-40" @click="showSuggestionModal = false"></div>
      <div class="relative bg-white rounded-xl shadow-2xl w-11/12 max-w-3xl max-h-[85vh] overflow-y-auto p-6">
        <div class="flex items-start justify-between mb-4">
          <h3 class="text-xl font-bold text-gray-900">
            Nutrition Suggestions — {{ selectedSuggestion?.range_key }} — {{
              formatDateTime(selectedSuggestion?.generated_at) }}
          </h3>
          <button class="text-gray-500 hover:text-gray-800" @click="showSuggestionModal = false">✕</button>
        </div>
        <div v-if="selectedSuggestion">
          <section class="mb-4" v-if="selectedSuggestion.suggestions?.overview">
            <h4 class="font-semibold mb-1">Overview</h4>
            <p class="text-gray-700">{{ selectedSuggestion.suggestions.overview }}</p>
          </section>
          <section class="mb-4" v-if="(selectedSuggestion.suggestions?.risks || []).length">
            <h4 class="font-semibold mb-1">Risks</h4>
            <ul class="list-disc list-inside text-gray-700">
              <li v-for="(r, i) in selectedSuggestion.suggestions.risks" :key="i">{{ r }}</li>
            </ul>
          </section>
          <section class="mb-4" v-if="selectedSuggestion.suggestions?.macro_targets">
            <h4 class="font-semibold mb-1">Macro Targets</h4>
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 text-sm">
              <div><span class="font-semibold">Calories:</span> {{ selectedSuggestion.suggestions.macro_targets.calories
                }}
              </div>
              <div><span class="font-semibold">Proteins:</span> {{ selectedSuggestion.suggestions.macro_targets.proteins
                }}
              </div>
              <div><span class="font-semibold">Carbs:</span> {{ selectedSuggestion.suggestions.macro_targets.carbs }}
              </div>
              <div><span class="font-semibold">Fat:</span> {{ selectedSuggestion.suggestions.macro_targets.fat }}</div>
              <div><span class="font-semibold">Sodium:</span> {{ selectedSuggestion.suggestions.macro_targets.sodium }}
              </div>
              <div><span class="font-semibold">Sugar:</span> {{ selectedSuggestion.suggestions.macro_targets.sugar }}
              </div>
            </div>
          </section>
          <section class="mb-4" v-if="selectedSuggestion.suggestions?.hydration_advice">
            <h4 class="font-semibold mb-1">Hydration Advice</h4>
            <p class="text-gray-700">{{ selectedSuggestion.suggestions.hydration_advice }}</p>
          </section>
          <section class="mb-4" v-if="(selectedSuggestion.suggestions?.meal_plan || []).length">
            <h4 class="font-semibold mb-1">Meal Plan</h4>
            <ul class="space-y-2">
              <li v-for="(m, i) in selectedSuggestion.suggestions.meal_plan" :key="i" class="p-3 bg-gray-50 rounded-lg">
                <div class="text-sm text-gray-500">{{ m.timeOfDay }}</div>
                <div class="font-semibold">{{ m.item }}</div>
                <div class="text-sm text-gray-600" v-if="m.rationale">{{ m.rationale }}</div>
              </li>
            </ul>
          </section>
          <section class="mb-4" v-if="selectedSuggestion.suggestions?.notes">
            <h4 class="font-semibold mb-1">Notes</h4>
            <p class="text-gray-700">{{ selectedSuggestion.suggestions.notes }}</p>
          </section>
          <div class="mt-4">
            </div>
        </div>
      </div>
    </div>

    <NewTaskModal :is-open="showNewTask" @close="showNewTask = false" @created="onTaskCreated" />
  </div>
</template>

<script>
import axios from 'axios'
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import AppCard from '@/components/ui/AppCard.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import NewTaskModal from '@/components/teacher/NewTaskModal.vue'

export default {
  name: 'ReportsView',
  components: { AppCard, AppButton, AppBadge, NewTaskModal },
  setup() {
    const route = useRoute()
    const placeholder = 'https://placehold.co/80x80?text=👤'

    const students = ref([])
    const selectedStudent = ref(null)
    const report = ref(null)
    const recentSuggestions = ref([])
    const showSuggestionModal = ref(false)
    const selectedSuggestion = ref(null)
    const showRaw = ref(false)
    const loading = ref(false)
    const error = ref('')
    const showNewTask = ref(false)

    const telLink = computed(() => {
      const raw = report.value?.emergency_contact_phone
      if (!raw) return ''
      try {
        const normalized = String(raw).trim().replace(/[^+\d]/g, '')
        return normalized ? `tel:${normalized}` : ''
      } catch {
        return ''
      }
    })

    function getAuthHeader() {
      const token = localStorage.getItem('token') || ''
      if (!token) return null
      const raw = token.replace(/^bearer\s+/i, '').replace(/^Bearer\s+/, '')
      return `Bearer ${raw}`
    }
    const API = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000' })
    API.interceptors.request.use(cfg => {
      const auth = getAuthHeader(); if (auth) cfg.headers.Authorization = auth; return cfg
    })

    async function loadStudents() {
      loading.value = true; error.value = ''
      try {
        const { data } = await API.get('/teacher/reports/students')
        students.value = Array.isArray(data) ? data : []
        // preselect via query
        const sid = route.query.student_id
        if (sid) {
          const s = students.value.find(x => x.student_id === sid)
          if (s) selectStudent(s)
        }
      } catch (e) {
        error.value = e.response?.data?.detail || 'Failed to load students'
      } finally { loading.value = false }
    }

    function selectStudent(s) {
      selectedStudent.value = s
      loadReport(s.student_id)
    }

    async function loadReport(studentId) {
      loading.value = true; error.value = ''; report.value = null
      try {
        const { data } = await API.get(`/teacher/reports/${studentId}`)
        report.value = data
        // also load recent nutrition suggestions for modal details
        await loadSuggestions(studentId)
      } catch (e) {
        error.value = e.response?.data?.detail || 'Failed to load report'
      } finally { loading.value = false }
    }

    async function loadSuggestions(studentId) {
      try {
        const { data } = await API.get(`/teacher/reports/${studentId}/nutrition_suggestions`, { params: { limit: 5 } })
        recentSuggestions.value = Array.isArray(data) ? data : []
      } catch (e) {
        // non-fatal; keep silent but available for debugging
        console.warn('Failed to load suggestions', e?.response?.data || e?.message)
        recentSuggestions.value = []
      }
    }

    function isNutritionEvent(e) {
      return typeof e?.what === 'string' && e.what.startsWith('Nutrition suggestions generated')
    }

    function openSuggestionByGeneratedAt(genAt) {
      if (!genAt) return
      const match = recentSuggestions.value.find(s => s.generated_at === genAt)
      if (match) {
        selectedSuggestion.value = match
        showSuggestionModal.value = true
        showRaw.value = false
      } else if (selectedStudent.value) {
        // fetch exact by generated_at
        API.get(`/teacher/reports/${selectedStudent.value.student_id}/nutrition_suggestions`, { params: { generated_at: genAt } })
          .then(({ data }) => {
            const rec = Array.isArray(data) ? data[0] : data
            if (rec) {
              selectedSuggestion.value = rec
              showSuggestionModal.value = true
              showRaw.value = false
            }
          })
          .catch(() => { })
      }
    }

    function formatDateTime(v) {
      try { const d = new Date(v); return d.toLocaleString() } catch { return String(v) }
    }
    const overallGrade = '—' // Placeholder; can be derived when scores are available

    onMounted(loadStudents)

    function latestSuggestion() {
      const genAt = report.value?.healthSummary?.latestNutrition?.generated_at
      if (!genAt) return recentSuggestions.value[0]
      return recentSuggestions.value.find(s => s.generated_at === genAt) || recentSuggestions.value[0]
    }

    function latestRiskLabel() {
      const s = latestSuggestion()
      const risks = s?.suggestions?.alerts
      if (Array.isArray(risks) && risks.length) {
        // pick first; could randomize if desired
        return risks[0]
      }
      return ''
    }

    function nutritionLabel() {
      const s = latestSuggestion()
      const risks = s?.suggestions?.risks
      if (Array.isArray(risks) && risks.length) {
        // pick first; could randomize if desired
        return risks
      }
      return []
    }

    function openLatestSuggestion() {
      const genAt = report.value?.healthSummary?.latestNutrition?.generated_at
      if (genAt) {
        openSuggestionByGeneratedAt(genAt)
      } else if (recentSuggestions.value[0]) {
        selectedSuggestion.value = recentSuggestions.value[0]
        showSuggestionModal.value = true
        showRaw.value = false
      }
    }

    function taskAssignedEvents() {
      const items = Array.isArray(report.value?.recentActivity) ? report.value.recentActivity : []
      return items.filter(e => typeof e?.what === 'string' && /(task assigned|assigned task)/i.test(e.what))
    }

    function taskTaskEvents() {
      const items = Array.isArray(report.value?.recentActivity) ? report.value.recentActivity : []
      return items.filter(e => {
        const w = e?.what || ''
        return /(task assigned|assigned task|completed task)/i.test(w) && !/^nutrition suggestions generated/i.test(w)
      })
    }

    function onTaskCreated() {
      // refresh report so academic metrics reflect the new assignment
      if (selectedStudent.value?.student_id) {
        loadReport(selectedStudent.value.student_id)
      }
    }

    return { placeholder, students, selectedStudent, report, loading, error, selectStudent, formatDateTime, overallGrade, recentSuggestions, showSuggestionModal, selectedSuggestion, showRaw, isNutritionEvent, openSuggestionByGeneratedAt, latestRiskLabel, nutritionLabel, openLatestSuggestion, showNewTask, onTaskCreated, taskAssignedEvents, taskTaskEvents, telLink }
  }
}
</script>