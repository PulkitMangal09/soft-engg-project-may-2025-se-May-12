<!-- src/views/teacher/MyStudentsView.vue -->
<template>
  <div class="min-h-screen bg-gray-50">
    <div class="mx-auto max-w-7xl px-4 py-8">
      <!-- Header + actions -->
      <div class="mb-6 flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">My Students</h1>
          <p class="text-gray-600">Overview of your classrooms and connections</p>
        </div>
        <div class="flex gap-3">
          <AppButton label="Generate Invite" icon="✨" variant="secondary" @click="openInviteModal()" />
          <AppButton label="Create Classroom" icon="➕" variant="primary" @click="openCreateModal" />
        </div>
      </div>

      <!-- Top Stats -->
      <div class="mb-8 grid grid-cols-1 gap-6 md:grid-cols-3">
        <div class="rounded-xl bg-white p-6 shadow">
          <p class="text-sm text-gray-500">Total Students</p>
          <p class="text-3xl font-bold text-gray-900">{{ totalStudents }}</p>
        </div>
        <div class="rounded-xl bg-white p-6 shadow">
          <p class="text-sm text-gray-500">Total Classrooms</p>
          <p class="text-3xl font-bold text-gray-900">{{ totalClassrooms }}</p>
        </div>
        <div class="rounded-xl bg-white p-6 shadow">
          <p class="text-sm text-gray-500">Active Classrooms</p>
          <p class="text-3xl font-bold text-gray-900">{{ activeClassrooms }}</p>
        </div>
      </div>

      <!-- Content -->
      <div class="grid grid-cols-1 gap-8 lg:grid-cols-3">
        <!-- Classrooms -->
        <div class="lg:col-span-2 rounded-xl bg-white p-6 shadow">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-xl font-bold text-gray-800">Your Classrooms</h2>
            <span class="text-sm text-gray-500">{{ classrooms.length }} listed</span>
          </div>

          <div v-if="loadingClassrooms" class="text-gray-500">Loading classrooms…</div>
          <div v-else-if="classrooms.length === 0" class="text-gray-500">No classrooms found.</div>

          <div v-else class="space-y-3">
            <div
              v-for="c in classrooms"
              :key="c.classroom_id"
              class="rounded-lg border p-4"
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
                  <p class="mt-1 text-xs text-gray-400">
                    Key: <code class="rounded bg-gray-100 px-1">{{ c.classroom_key }}</code>
                  </p>
                </div>
                <div class="text-right">
                  <div
                    class="inline-flex items-center rounded-full px-2 py-1 text-xs"
                    :class="c.is_active ? 'bg-green-50 text-green-700' : 'bg-gray-100 text-gray-600'"
                  >
                    {{ c.is_active ? 'Active' : 'Inactive' }}
                  </div>
                  <div v-if="c.created_at" class="mt-1 text-xs text-gray-400">
                    Created: {{ formatDate(c.created_at) }}
                  </div>
                </div>
              </div>

              <div class="mt-3 flex flex-wrap gap-2">
                <AppButton label="Invite Student" size="sm" variant="secondary" @click="openInviteModal(c, 'teacher_student')" />
                <AppButton label="Invite Parent" size="sm" variant="secondary" @click="openInviteModal(c, 'parent_student')" />
                <AppButton label="Edit" size="sm" variant="secondary" @click="openEdit(c)" />
                <AppButton label="Delete" size="sm" variant="error" @click="askDelete(c)" />
              </div>
            </div>
          </div>
        </div>

        <!-- RIGHT COLUMN: Connections (accepted) + Pending Requests -->
        <div class="rounded-xl bg-white p-6 shadow">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-xl font-bold text-gray-800">Connections</h2>
            <span class="text-sm text-gray-500">{{ acceptedRequests.length }} total</span>
          </div>

          <div v-if="loadingAccepted" class="text-gray-500">Loading connections…</div>

          <template v-else>
            <!-- Students -->
            <div class="mb-6">
              <h3 class="mb-2 text-sm font-semibold text-gray-700">
                Students ({{ studentsAccepted.length }})
              </h3>

              <div v-if="studentsAccepted.length === 0" class="text-sm text-gray-500">
                No students connected yet.
              </div>

              <ul v-else class="max-h-64 space-y-2 overflow-auto pr-1">
                <li
                  v-for="r in studentsAccepted"
                  :key="r.request_id"
                  class="flex items-center justify-between rounded-md border px-3 py-2"
                >
                  <div>
                    <div class="font-medium text-gray-800">
                      {{ r.name || r.student_name || r.requester_name || 'Student' }}
                    </div>
                    <div class="text-xs text-gray-500">
                      <span v-if="r.email">{{ r.email }}</span>
                      <span v-if="r.classroom_name"> • {{ r.classroom_name }}</span>
                      <span v-if="r.grade_level"> • Grade: {{ r.grade_level }}</span>
                    </div>
                  </div>
                  <span class="rounded-full bg-green-50 px-2 py-0.5 text-xs text-green-700">accepted</span>
                </li>
              </ul>
            </div>

            <!-- Parents -->
            <div>
              <h3 class="mb-2 text-sm font-semibold text-gray-700">
                Parents ({{ parentsAccepted.length }})
              </h3>

              <div v-if="parentsAccepted.length === 0" class="text-sm text-gray-500">
                No parents connected yet.
              </div>

              <ul v-else class="max-h-64 space-y-2 overflow-auto pr-1">
                <li
                  v-for="r in parentsAccepted"
                  :key="r.request_id"
                  class="flex items-center justify-between rounded-md border px-3 py-2"
                >
                  <div>
                    <div class="font-medium text-gray-800">
                      {{ r.name || r.parent_name || r.requester_name || 'Parent' }}
                    </div>
                    <div class="text-xs text-gray-500">
                      <span v-if="r.email">{{ r.email }}</span>
                      <span v-if="r.child_name"> • Child: {{ r.child_name }}</span>
                    </div>
                  </div>
                  <span class="rounded-full bg-green-50 px-2 py-0.5 text-xs text-green-700">accepted</span>
                </li>
              </ul>
            </div>
          </template>

          <!-- Pending requests -->
          <div class="mt-8 border-t pt-4">
            <div class="mb-2 flex items-center justify-between">
              <h3 class="text-sm font-semibold text-gray-700">
                Connection Requests
              </h3>
              <AppButton
                v-if="pendingRequests.length > 0"
                size="sm"
                label="Accept All"
                variant="primary"
                :disabled="respondingAll"
                @click="acceptAll"
              />
            </div>

            <div v-if="loadingRequests" class="text-gray-500">Loading requests…</div>
            <div v-else-if="pendingRequests.length === 0" class="text-sm text-gray-500">No pending requests.</div>

            <div v-else class="space-y-2">
              <div
                v-for="req in pendingRequests"
                :key="req.request_id"
                class="flex items-start justify-between rounded-md border px-3 py-2"
              >
                <div class="mr-3 flex-1">
                  <p class="font-medium text-gray-900">
                    {{ req.display_name }}
                    <span class="ml-2 rounded bg-gray-100 px-2 py-0.5 text-xs text-gray-600">
                      {{ req.roleLabel }}
                    </span>
                  </p>
                  <p class="text-xs text-gray-600">
                    {{ req.display_email }}
                    <span v-if="req.classroom_name" class="mx-2">•</span>
                    <span v-if="req.classroom_name" class="text-gray-500">Classroom: {{ req.classroom_name }}</span>
                  </p>
                  <p v-if="req.message" class="mt-1 text-xs text-gray-500">“{{ req.message }}”</p>
                  <p class="mt-1 text-[11px] text-gray-400">Requested: {{ formatDateTime(req.requested_at) }}</p>
                </div>

                <div class="flex gap-2">
                  <AppButton
                    size="sm"
                    label="Accept"
                    variant="success"
                    :disabled="req._busy"
                    @click="respond(req.request_id, 'accepted')"
                  />
                  <AppButton
                    size="sm"
                    label="Reject"
                    variant="error"
                    :disabled="req._busy"
                    @click="respond(req.request_id, 'rejected')"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- /RIGHT COLUMN -->
      </div>
    </div>

    <!-- Create/Edit modal -->
    <AppModal :is-open="isEditOpen" @close="closeEdit" :title="editId ? 'Edit Classroom' : 'Create Classroom'">
      <form @submit.prevent="submitEdit" class="space-y-4">
        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">Name</label>
          <input v-model.trim="form.name" type="text" required class="w-full rounded-md border px-3 py-2">
        </div>
        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">Subject</label>
          <input v-model.trim="form.subject" type="text" required class="w-full rounded-md border px-3 py-2">
        </div>
        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">School</label>
          <input v-model.trim="form.school_name" type="text" class="w-full rounded-md border px-3 py-2" placeholder="optional">
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Grade Level</label>
            <input v-model.trim="form.grade_level" type="text" class="w-full rounded-md border px-3 py-2" placeholder="e.g., 4th year">
          </div>
          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Max Students</label>
            <input v-model.number="form.max_students" type="number" min="1" class="w-full rounded-md border px-3 py-2">
          </div>
        </div>

        <div class="pt-2 flex justify-end gap-3">
          <AppButton label="Cancel" variant="secondary" type="button" @click="closeEdit" />
          <AppButton :label="editId ? 'Save' : 'Create'" variant="primary" type="submit" :disabled="savingEdit" />
        </div>
      </form>
    </AppModal>

    <!-- Delete confirm -->
    <AppModal :is-open="isDeleteOpen" @close="isDeleteOpen=false" title="Delete Classroom">
      <p class="text-gray-700">Are you sure you want to delete this classroom?</p>
      <div class="mt-6 flex justify-end gap-3">
        <AppButton label="Cancel" variant="secondary" @click="isDeleteOpen=false" />
        <AppButton label="Delete" variant="error" @click="confirmDelete" :disabled="deleting" />
      </div>
    </AppModal>

    <!-- Invite modal -->
    <TeacherInviteModal
      :is-open="isInviteOpen"
      @close="isInviteOpen=false"
      :classrooms="classrooms"
      :preselected-classroom-id="inviteClassroomId"
      :default-type="inviteDefaultType"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import AppButton from '@/components/ui/AppButton.vue'
import AppModal from '@/components/ui/AppModal.vue'
import TeacherInviteModal from '@/components/invitations/TeacherInviteModal.vue'
import { teacherService } from '@/services/teacherService'
import { requestsService } from '@/services/requestsService'

/* ---------- auth ---------- */
const store = useStore()
const token = computed(() => store.getters['auth/token'] || store.state.auth?.token || '')

/* ---------- classrooms + metrics ---------- */
const loadingClassrooms = ref(false)
const loadingMetrics = ref(false)
const classrooms = ref([])
const studentsMetrics = ref({
  total_classrooms: 0,
  active_classrooms: 0,
  total_students: 0,
})

const totalStudents = computed(() => studentsMetrics.value?.total_students ?? 0)
const totalClassrooms = computed(() => studentsMetrics.value?.total_classrooms ?? classrooms.value.length)
const activeClassrooms = computed(() => studentsMetrics.value?.active_classrooms ?? classrooms.value.filter(c => c.is_active !== false).length)

const loadClassrooms = async () => {
  loadingClassrooms.value = true
  try {
    classrooms.value = token.value ? await teacherService.getClassrooms(token.value) : []
  } catch (e) {
    console.error('Error loading classrooms:', e)
    classrooms.value = []
  } finally {
    loadingClassrooms.value = false
  }
}

const loadMetrics = async () => {
  loadingMetrics.value = true
  try {
    studentsMetrics.value = token.value
      ? await teacherService.getStudentsMetrics(token.value)
      : { total_classrooms: 0, active_classrooms: 0, total_students: 0 }
  } catch (e) {
    console.error('Error loading metrics:', e)
    studentsMetrics.value = { total_classrooms: 0, active_classrooms: 0, total_students: 0 }
  } finally {
    loadingMetrics.value = false
  }
}

/* ---------- connections (accepted) & pending requests ---------- */
const loadingAccepted = ref(false)
const acceptedRequests = ref([])

const loadingRequests = ref(false)
const pendingRequests = ref([])
const respondingAll = ref(false)

const studentsAccepted = computed(() => acceptedRequests.value.filter(r => (r.requester_type || r.type) === 'student'))
const parentsAccepted  = computed(() => acceptedRequests.value.filter(r => (r.requester_type || r.type) === 'parent'))

const loadAccepted = async () => {
  loadingAccepted.value = true
  try {
    acceptedRequests.value = token.value
      ? await requestsService.listRequests(token.value, 'accepted')
      : []
  } catch (e) {
    console.error('Error loading accepted connections:', e)
    acceptedRequests.value = []
  } finally {
    loadingAccepted.value = false
  }
}

const loadRequests = async () => {
  loadingRequests.value = true
  try {
    pendingRequests.value = token.value
      ? await requestsService.listRequests(token.value, 'pending')
      : []
  } catch (e) {
    console.error('Error loading pending requests:', e)
    pendingRequests.value = []
  } finally {
    loadingRequests.value = false
  }
}

const respond = async (id, action) => {
  if (!token.value) return
  try {
    await requestsService.respondToRequest(id, action, token.value)
    await Promise.all([loadRequests(), loadAccepted(), loadMetrics()])
  } catch (e) {
    const msg = e?.response?.data?.detail || 'Failed to update request'
    console.error('Respond failed:', e?.response?.data || e)
    store.dispatch?.('ui/showToast', { title: 'Error', message: msg, type: 'error' })
  }
}

const acceptAll = async () => {
  if (!token.value || pendingRequests.value.length === 0) return
  respondingAll.value = true
  try {
    const ids = pendingRequests.value.map(r => r.request_id)
    await Promise.all(ids.map(id => requestsService.respondToRequest(id, 'accepted', token.value)))
    await Promise.all([loadRequests(), loadAccepted(), loadMetrics()])
    store.dispatch?.('ui/showToast', { title: 'All requests accepted', message: 'Everyone is in 🎉', type: 'success' })
  } catch (e) {
    console.error('Accept all failed:', e)
  } finally {
    respondingAll.value = false
  }
}

/* ---------- create / edit / delete classroom ---------- */
const isEditOpen = ref(false)
const editId = ref(null)
const form = ref({ name: '', subject: '', school_name: '', grade_level: '', max_students: null })
const savingEdit = ref(false)

const isDeleteOpen = ref(false)
const pendingDeleteId = ref(null)
const deleting = ref(false)

const openCreateModal = () => {
  editId.value = null
  form.value = { name: '', subject: '', school_name: '', grade_level: '', max_students: null }
  isEditOpen.value = true
}
const openEdit = (row) => {
  editId.value = row.classroom_id
  form.value = {
    name: row.classroom_name || row.name || '',
    subject: row.subject || '',
    school_name: row.school_name || '',
    grade_level: row.grade_level || '',
    max_students: row.max_students ?? null
  }
  isEditOpen.value = true
}
const closeEdit = () => { isEditOpen.value = false; savingEdit.value = false }

const submitEdit = async () => {
  if (!token.value) return
  try {
    savingEdit.value = true
    if (editId.value) {
      await teacherService.updateClassroom(editId.value, { ...form.value }, token.value)
    } else {
      await teacherService.createClassroom({ ...form.value }, token.value)
    }
    closeEdit()
    await refreshAll()
  } catch (e) {
    console.error('Save classroom failed:', e)
  } finally {
    savingEdit.value = false
  }
}

const askDelete = (row) => { pendingDeleteId.value = row.classroom_id; isDeleteOpen.value = true }

const confirmDelete = async () => {
  if (!pendingDeleteId.value || !token.value) return
  try {
    deleting.value = true
    await teacherService.deleteClassroom(pendingDeleteId.value, token.value, { hard: true })
    isDeleteOpen.value = false
    pendingDeleteId.value = null
    await refreshAll()
  } catch (e) {
    console.error('Delete failed:', e)
  } finally {
    deleting.value = false
  }
}

/* ---------- invites ---------- */
const isInviteOpen = ref(false)
const inviteClassroomId = ref(null)
const inviteDefaultType = ref('teacher_student')

const openInviteModal = (row = null, defaultType = 'teacher_student') => {
  inviteClassroomId.value = row?.classroom_id || null
  inviteDefaultType.value = defaultType
  isInviteOpen.value = true
}

/* ---------- utils ---------- */
const formatDate = (value) => {
  try { if (!value) return ''; const d = new Date(value); return Number.isNaN(d.getTime()) ? String(value) : d.toLocaleDateString() }
  catch { return String(value) }
}
const formatDateTime = (value) => {
  try { if (!value) return ''; const d = new Date(value); return Number.isNaN(d.getTime()) ? String(value) : d.toLocaleString() }
  catch { return String(value) }
}

/* ---------- load all ---------- */
const refreshAll = async () => {
  await Promise.all([loadClassrooms(), loadMetrics(), loadAccepted(), loadRequests()])
}
onMounted(refreshAll)
</script>
