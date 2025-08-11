<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center py-6 px-2 md:px-0">
    <!-- Toasts -->
    <div class="fixed top-4 right-4 space-y-2 z-50" v-if="toasts.length">
      <div v-for="t in toasts" :key="t.id" class="px-3 py-2 rounded shadow text-sm"
        :class="t.type === 'error' ? 'bg-red-600 text-white' : 'bg-green-600 text-white'">
        {{ t.message }}
      </div>
    </div>
    <div class="bg-white rounded-xl shadow p-6 w-full max-w-3xl">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold">Medical Conditions & Medications</h2>
        <div class="text-sm text-gray-500" v-if="loading">Loading...</div>
      </div>

      <div v-if="error" class="bg-red-50 text-red-700 p-2 rounded mb-4 text-sm">{{ error }}</div>

      <!-- Conditions -->
      <div class="mb-6">
        <div class="flex items-center justify-between mb-2">
          <div class="font-semibold">Conditions</div>
          <button class="btn-secondary" @click="showAddCondition = !showAddCondition">{{ showAddCondition ? 'Close' :
            'Add Condition' }}</button>
        </div>

        <div v-if="showAddCondition" class="bg-gray-50 p-3 rounded mb-3 grid grid-cols-1 md:grid-cols-3 gap-2">
          <input v-model="newCondition.condition_name" class="input" placeholder="Condition name" />
          <select v-model="newCondition.severity" class="input">
            <option disabled value="">Severity</option>
            <option value="mild">Mild</option>
            <option value="moderate">Moderate</option>
            <option value="severe">Severe</option>
          </select>
          <input v-model="newCondition.diagnosed_date" type="date" class="input" />
          <input v-model="newCondition.doctor_clinic" class="input md:col-span-2" placeholder="Doctor/Clinic" />
          <input v-model="newCondition.dietary_restrictions" class="input md:col-span-3"
            placeholder="Dietary restrictions" />
          <input v-model="newCondition.symptoms_to_monitor" class="input md:col-span-3"
            placeholder="Symptoms to monitor" />
          <div class="md:col-span-3 flex gap-2">
            <button class="btn-primary" @click="onCreateCondition">Save</button>
            <button class="btn-secondary" @click="resetConditionForm">Reset</button>
          </div>
        </div>

        <div v-if="conditions.length === 0" class="text-sm text-gray-500">No conditions yet.</div>
        <div v-else class="space-y-2">
          <div v-for="c in conditions" :key="c.condition_id" class="border rounded p-3">
            <div class="flex items-center justify-between">
              <div class="font-medium">
                {{ c.condition_name }}
                <span class="ml-2 text-xs px-2 py-0.5 rounded-full" :class="{
                  'bg-green-100 text-green-700': c.severity === 'mild',
                  'bg-yellow-100 text-yellow-700': c.severity === 'moderate',
                  'bg-red-100 text-red-700': c.severity === 'severe'
                }">{{ c.severity }}</span>
              </div>
              <div class="flex gap-2">
                <button class="text-xs text-blue-600 hover:underline" @click="selectCondition(c)">Add
                  Medication</button>
                <button class="text-xs text-red-600 hover:underline"
                  @click="onDeleteCondition(c.condition_id)">Delete</button>
              </div>
            </div>
            <div class="text-xs text-gray-600 mt-1">
              <span v-if="c.diagnosed_date">Diagnosed: {{ formatDate(c.diagnosed_date) }}</span>
              <span v-if="c.doctor_clinic"> • {{ c.doctor_clinic }}</span>
              <div v-if="c.dietary_restrictions">Diet: {{ c.dietary_restrictions }}</div>
              <div v-if="c.symptoms_to_monitor">Monitor: {{ c.symptoms_to_monitor }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Medications -->
      <div>
        <div class="flex items-center justify-between mb-2">
          <div class="font-semibold">Medications</div>
          <button class="btn-secondary" @click="showAddMedication = !showAddMedication">{{ showAddMedication ? 'Close' :
            'Add Medication' }}</button>
        </div>

        <div v-if="showAddMedication" class="bg-gray-50 p-3 rounded mb-3 grid grid-cols-1 md:grid-cols-3 gap-2">
          <select v-model="newMedication.condition_id" class="input">
            <option disabled value="">Condition (optional)</option>
            <option v-for="c in conditions" :key="c.condition_id" :value="c.condition_id">{{ c.condition_name }}
            </option>
          </select>
          <input v-model="newMedication.medication_name" class="input" placeholder="Medication name" />
          <input v-model="newMedication.dosage" class="input" placeholder="Dosage" />
          <input v-model="newMedication.frequency" class="input" placeholder="Frequency" />
          <input v-model="newMedication.start_date" type="date" class="input" />
          <input v-model="newMedication.end_date" type="date" class="input" />
          <input v-model="newMedication.prescribing_doctor" class="input md:col-span-2"
            placeholder="Prescribing doctor" />
          <input v-model="newMedication.instructions" class="input md:col-span-3" placeholder="Instructions" />
          <div class="md:col-span-3 flex gap-2">
            <button class="btn-primary" @click="onCreateMedication">Save</button>
            <button class="btn-secondary" @click="resetMedicationForm">Reset</button>
          </div>
        </div>

        <div v-if="medications.length === 0" class="text-sm text-gray-500">No medications yet.</div>
        <div v-else class="space-y-2">
          <div v-for="m in medications" :key="m.medication_id" class="border rounded p-3">
            <div class="flex items-center justify-between">
              <div class="font-medium">{{ m.medication_name }}<span v-if="m.dosage" class="text-sm text-gray-600"> • {{
                  m.dosage }}</span></div>
              <div class="flex gap-2">
                <button class="text-xs text-blue-700 hover:underline" @click="toggleLogs(m)">{{
                  logsOpen[m.medication_id] ? 'Hide Logs' : 'Show Logs' }}</button>
                <button class="text-xs text-red-600 hover:underline"
                  @click="onDeleteMedication(m.medication_id)">Delete</button>
              </div>
            </div>
            <div class="text-xs text-gray-600 mt-1">
              <div v-if="m.frequency">Frequency: {{ m.frequency }}</div>
              <div>
                <span v-if="m.start_date">Start: {{ formatDate(m.start_date) }}</span>
                <span v-if="m.end_date"> • End: {{ formatDate(m.end_date) }}</span>
              </div>
              <div v-if="m.prescribing_doctor">Doctor: {{ m.prescribing_doctor }}</div>
              <div v-if="m.instructions">Instructions: {{ m.instructions }}</div>
            </div>

            <!-- Logs Panel -->
            <div v-if="logsOpen[m.medication_id]" class="mt-3 border-t pt-3">
              <div class="flex items-center justify-between mb-2">
                <div class="font-medium text-sm">Intake Logs</div>
                <div class="text-xs text-gray-500" v-if="loadingLogs[m.medication_id]">Loading logs...</div>
              </div>

              <div v-if="(logsByMed[m.medication_id] || []).length === 0" class="text-xs text-gray-500">No logs yet.
              </div>
              <ul v-else class="space-y-1 text-xs">
                <li v-for="log in logsByMed[m.medication_id]" :key="log.log_id"
                  class="flex items-center justify-between">
                  <div>
                    <span class="font-medium">{{ log.quantity_taken || '—' }}</span>
                    <span class="text-gray-600"> • {{ formatDateTime(log.taken_at) }}</span>
                    <span v-if="log.notes" class="text-gray-600"> • {{ log.notes }}</span>
                  </div>
                </li>
              </ul>

              <!-- Inline Log Form -->
              <div class="mt-3 grid grid-cols-1 md:grid-cols-4 gap-2">
                <input v-model="logForms[m.medication_id].quantity" class="input"
                  placeholder="Quantity (e.g., 1 pill)" />
                <input v-model="logForms[m.medication_id].notes" class="input md:col-span-2"
                  placeholder="Notes (optional)" />
                <input v-model="logForms[m.medication_id].taken_at" type="datetime-local" class="input" />
                <div class="md:col-span-4">
                  <button class="btn-primary" @click="onCreateLog(m)">Add Log</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="text-xs text-gray-400 mt-4">Medical Conditions</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  getConditions, createCondition, deleteCondition,
  getMedications, createMedication, deleteMedication,
  getMedicationLogs, createMedicationLog
} from '@/services/medicalService'

const loading = ref(false)
const error = ref('')
const conditions = ref([])
const medications = ref([])

// Toasts
const toasts = ref([])
function toast(message, type = 'success', duration = 2500) {
  const id = Date.now() + Math.random()
  toasts.value.push({ id, message, type })
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }, duration)
}

// UI state
const showAddCondition = ref(false)
const showAddMedication = ref(false)
const selectedConditionId = ref('')

// Logs state per medication
const logsOpen = ref({})
const logsByMed = ref({})
const loadingLogs = ref({})
const logForms = ref({})

function ensureLogForm(medId) {
  if (!logForms.value[medId]) {
    logForms.value = { ...logForms.value, [medId]: { quantity: '', notes: '', taken_at: '' } }
  }
}

// Forms
const newCondition = ref({
  condition_name: '',
  severity: '',
  diagnosed_date: '',
  doctor_clinic: '',
  dietary_restrictions: '',
  symptoms_to_monitor: '',
  is_active: true,
})

const newMedication = ref({
  condition_id: '',
  medication_name: '',
  dosage: '',
  frequency: '',
  start_date: '',
  end_date: '',
  prescribing_doctor: '',
  instructions: '',
  is_active: true,
})

function resetConditionForm() {
  newCondition.value = {
    condition_name: '', severity: '', diagnosed_date: '', doctor_clinic: '',
    dietary_restrictions: '', symptoms_to_monitor: '', is_active: true,
  }
}

function resetMedicationForm() {
  newMedication.value = {
    condition_id: '', medication_name: '', dosage: '', frequency: '',
    start_date: '', end_date: '', prescribing_doctor: '', instructions: '', is_active: true,
  }
}

function formatDate(d) {
  if (!d) return ''
  try { return new Date(d).toLocaleDateString() } catch { return d }
}

function formatDateTime(d) {
  if (!d) return ''
  try { return new Date(d).toLocaleString() } catch { return d }
}

function selectCondition(c) {
  selectedConditionId.value = c.condition_id
  showAddMedication.value = true
  newMedication.value.condition_id = c.condition_id
}

async function loadAll() {
  loading.value = true
  error.value = ''
  try {
    const [cond, meds] = await Promise.all([
      getConditions(),
      getMedications(),
    ])
    conditions.value = cond
    medications.value = meds
    // initialize forms for each med
    meds.forEach(m => ensureLogForm(m.medication_id))
  } catch (e) {
    error.value = e?.response?.data?.detail || e?.message || 'Failed to load data'
    toast(error.value, 'error')
  } finally {
    loading.value = false
  }
}

async function onCreateCondition() {
  if (!newCondition.value.condition_name || !newCondition.value.severity) return
  try {
    await createCondition({
      ...newCondition.value,
      diagnosed_date: newCondition.value.diagnosed_date || null,
    })
    resetConditionForm()
    showAddCondition.value = false
    await loadAll()
    toast('Condition created')
  } catch (e) {
    error.value = e?.response?.data?.detail || 'Failed to create condition'
    toast(error.value, 'error')
  }
}

async function onDeleteCondition(id) {
  try {
    await deleteCondition(id)
    await loadAll()
    toast('Condition deleted')
  } catch (e) {
    error.value = e?.response?.data?.detail || 'Failed to delete condition'
    toast(error.value, 'error')
  }
}

async function onCreateMedication() {
  if (!newMedication.value.medication_name) return
  try {
    await createMedication({
      ...newMedication.value,
      condition_id: newMedication.value.condition_id || null,
      start_date: newMedication.value.start_date || null,
      end_date: newMedication.value.end_date || null,
    })
    resetMedicationForm()
    showAddMedication.value = false
    await loadAll()
    toast('Medication added')
  } catch (e) {
    error.value = e?.response?.data?.detail || 'Failed to create medication'
    toast(error.value, 'error')
  }
}

async function onDeleteMedication(id) {
  try {
    await deleteMedication(id)
    await loadAll()
    toast('Medication deleted')
  } catch (e) {
    error.value = e?.response?.data?.detail || 'Failed to delete medication'
    toast(error.value, 'error')
  }
}

async function toggleLogs(med) {
  const id = med.medication_id
  // ensure form exists before rendering panel
  ensureLogForm(id)
  const isOpen = !!logsOpen.value[id]
  logsOpen.value = { ...logsOpen.value, [id]: !isOpen }
  if (!isOpen) {
    // opening: load logs if not present
    loadingLogs.value = { ...loadingLogs.value, [id]: true }
    try {
      const logs = await getMedicationLogs(id)
      logsByMed.value = { ...logsByMed.value, [id]: logs }
    } catch (e) {
      const msg = e?.response?.data?.detail || 'Failed to load logs'
      error.value = msg
      toast(msg, 'error')
    } finally {
      loadingLogs.value = { ...loadingLogs.value, [id]: false }
    }
  }
}

async function onCreateLog(med) {
  const id = med.medication_id
  ensureLogForm(id)
  const form = logForms.value[id]
  if (!form.quantity && !form.notes) {
    toast('Enter quantity or notes', 'error')
    return
  }
  try {
    await createMedicationLog(id, {
      quantity_taken: form.quantity || null,
      notes: form.notes || null,
      taken_at: form.taken_at ? new Date(form.taken_at).toISOString() : null,
    })
    // reload logs
    const logs = await getMedicationLogs(id)
    logsByMed.value = { ...logsByMed.value, [id]: logs }
    // reset form
    logForms.value = { ...logForms.value, [id]: { quantity: '', notes: '', taken_at: '' } }
    toast('Log added')
  } catch (e) {
    const msg = e?.response?.data?.detail || 'Failed to add log'
    error.value = msg
    toast(msg, 'error')
  }
}

onMounted(loadAll)
</script>