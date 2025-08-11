<template>
  <div class="p-6 md:p-8 bg-gray-100 min-h-screen">
    <!-- Header -->
    <div class="mb-8 flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Teacher's Dashboard</h1>
        <p class="text-gray-600 mt-1">Welcome back, Mrs. Johnson!</p>
      </div>
      <div class="flex gap-3">
        <AppButton label="Generate Invitation Code" icon="🔗" variant="secondary" @click="openInvite()" />
        <AppButton label="Assign New Task" icon="➕" variant="primary" />
      </div>
    </div>

    <!-- Key Metrics -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
      <AppCard icon="🎓" title="Total Students" :subtitle="`${totalClassrooms} Classroom${totalClassrooms !== 1 ? 's' : ''}`">
        <div class="text-right">
          <p class="text-3xl font-bold text-gray-800">{{ totalStudents }}</p>
          <p class="text-sm text-gray-500">Students</p>
        </div>
      </AppCard>

      <AppCard icon="🔔" title="Health Alerts" variant="error">
        <div class="text-right">
          <p class="text-3xl font-bold text-red-500">0</p>
          <p class="text-sm text-gray-500">Active</p>
        </div>
      </AppCard>

      <AppCard icon="📝" title="Overdue Tasks" variant="warning">
        <div class="text-right">
          <p class="text-3xl font-bold text-amber-500">0</p>
          <p class="text-sm text-gray-500">Need Attention</p>
        </div>
        <template #footer>
          <div class="flex justify-end">
            <router-link to="/teacher/tasks">
              <AppButton label="View All Tasks" variant="secondary" size="sm" />
            </router-link>
          </div>
        </template>
      </AppCard>

      <AppCard icon="📊" title="Class Average" variant="success">
        <div class="text-right">
          <p class="text-3xl font-bold text-emerald-500">N/A</p>
          <p class="text-sm text-gray-500">Performance</p>
        </div>
      </AppCard>
    </div>

    <!-- My Students (summary) -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <AppCard title="Your Classrooms" :subtitle="`${classrooms.length} listed`">
          <template #default>
            <div v-if="loadingClassrooms" class="text-gray-500">Loading classrooms…</div>
            <div v-else-if="classrooms.length === 0" class="text-gray-500">No classrooms found.</div>
            <div v-else class="space-y-3">
              <div
                v-for="c in classrooms"
                :key="c.classroom_id"
                class="border rounded-lg p-4"
              >
                <div class="flex items-start justify-between">
                  <div>
                    <p class="font-semibold text-gray-900">
                      {{ c.classroom_name || c.name || 'Untitled Classroom' }}
                    </p>
                    <p class="text-sm text-gray-600">
                      <span v-if="c.subject">Subject: {{ c.subject }}</span>
                      <span v-if="c.subject && c.grade_level" class="mx-2">•</span>
                      <span v-if="c.grade_level">Grade: {{ c.grade_level }}</span>
                    </p>
                    <p v-if="c.school_name" class="text-sm text-gray-500">{{ c.school_name }}</p>
                    <p class="text-xs text-gray-400 mt-1">
                      Key: <code class="bg-gray-100 px-1 rounded">{{ c.classroom_key }}</code>
                    </p>
                  </div>
                  <div class="text-right">
                    <div
                      class="inline-flex items-center px-2 py-1 rounded-full text-xs"
                      :class="c.is_active ? 'bg-green-50 text-green-700' : 'bg-gray-100 text-gray-600'"
                    >
                      {{ c.is_active ? 'Active' : 'Inactive' }}
                    </div>
                    <div class="text-xs text-gray-400 mt-1" v-if="c.created_at">
                      Created: {{ formatDate(c.created_at) }}
                    </div>
                  </div>
                </div>

                <div class="mt-3 flex flex-wrap gap-2">
                  <AppButton label="Invite Student" size="sm" variant="secondary" @click="openInvite(c, 'teacher_student')" />
                  <AppButton label="Invite Parent" size="sm" variant="secondary" @click="openInvite(c, 'parent_student')" />
                </div>
              </div>
            </div>
          </template>
          <template #footer>
            <div class="flex justify-end">
              <router-link to="/teacher/students">
                <AppButton label="Manage Classrooms" variant="primary" />
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
                <div
                  v-for="row in gradeBuckets"
                  :key="row.grade"
                  class="flex items-center justify-between border rounded-lg px-3 py-2"
                >
                  <div class="font-medium text-gray-800">Grade {{ row.grade }}</div>
                  <div class="text-gray-600">{{ row.count }} students</div>
                </div>
              </div>
            </div>
          </template>
        </AppCard>
      </div>
    </div>

    <!-- Invite Modal -->
    <TeacherInviteModal
      :is-open="inviteOpen"
      :classrooms="classrooms"
      :default-type="inviteDefaults.type"
      :preselected-classroom-id="inviteDefaults.classroomId"
      @close="inviteOpen = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import AppCard from '@/components/ui/AppCard.vue'
import AppButton from '@/components/ui/AppButton.vue'
import TeacherInviteModal from '@/components/invitations/TeacherInviteModal.vue'
import { teacherService } from '@/services/teacherService'

const store = useStore()
const token = computed(() => store.getters['auth/token'] || store.state.auth?.token || '')

const classrooms = ref([])
const studentsMetrics = ref({
  total_classrooms: 0,
  active_classrooms: 0,
  total_students: 0,
  by_grade_level: {}
})
const loadingClassrooms = ref(false)
const loadingMetrics = ref(false)

const totalStudents = computed(() => studentsMetrics.value?.total_students ?? 0)
const totalClassrooms = computed(() => studentsMetrics.value?.total_classrooms ?? 0)

const gradeBuckets = computed(() => {
  const map = studentsMetrics.value?.by_grade_level || {}
  return Object.entries(map)
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
      token.value ? teacherService.getStudentsMetrics(token.value) : null
    ])
    classrooms.value = Array.isArray(cls) ? cls : []
    studentsMetrics.value = metrics || { total_classrooms: 0, active_classrooms: 0, total_students: 0, by_grade_level: {} }
  } catch (e) {
    console.error('Dashboard load error:', e)
    classrooms.value = []
  } finally {
    loadingClassrooms.value = false
    loadingMetrics.value = false
  }
}

onMounted(loadData)

// invite modal
const inviteOpen = ref(false)
const inviteDefaults = ref({ type: 'teacher_student', classroomId: null })
const openInvite = (row = null, type = 'teacher_student') => {
  inviteDefaults.value = { type, classroomId: row?.classroom_id || classrooms.value?.[0]?.classroom_id || null }
  inviteOpen.value = true
}
const openInviteFromHeader = () => openInvite()

// utils
const formatDate = (v) => {
  try {
    if (!v) return ''
    const d = new Date(v)
    return Number.isNaN(d.getTime()) ? String(v) : d.toLocaleDateString()
  } catch { return String(v) }
}
</script>
