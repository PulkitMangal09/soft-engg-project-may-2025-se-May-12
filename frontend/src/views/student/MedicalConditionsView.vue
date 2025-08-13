<template>
  <div class="min-h-screen bg-gray-100 flex flex-col items-center py-8 px-4 relative">
    
    <button
      @click="$router.go(-1)"
      class="absolute top-4 left-4 z-10 w-10 h-10 flex items-center justify-center rounded-full bg-white text-gray-600 shadow-md hover:bg-gray-200 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-gray-300 transition-all"
      aria-label="Go Back"
    >
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-6 h-6">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>
    
    <div class="fixed top-4 right-4 space-y-2 z-50">
      <div v-for="t in toasts" :key="t.id" class="px-4 py-2 rounded-lg shadow-lg text-sm font-medium"
        :class="t.type === 'error' ? 'bg-red-600 text-white' : 'bg-green-600 text-white'">
        {{ t.message }}
      </div>
    </div>
    
    <div class="w-full max-w-4xl space-y-8">
      <header class="text-center">
        <h1 class="text-4xl font-bold text-gray-800">Medical Records 🩺</h1>
        <p class="mt-2 text-gray-500">View and manage your medical conditions and medications.</p>
      </header>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        <div>
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-2xl font-bold text-gray-700">Conditions</h2>
            <button class="btn-secondary" @click="showAddCondition = !showAddCondition">
              <span v-if="showAddCondition">Close</span>
              <span v-else>+ Add Condition</span>
            </button>
          </div>
          
          <div v-if="showAddCondition" class="bg-white rounded-lg shadow-sm p-4 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input v-model="newCondition.condition_name" class="input-field col-span-1" placeholder="Condition name" />
              <select v-model="newCondition.severity" class="input-field col-span-1">
                <option disabled value="">Severity</option>
                <option value="mild">Mild</option>
                <option value="moderate">Moderate</option>
                <option value="severe">Severe</option>
              </select>
              <input v-model="newCondition.diagnosed_date" type="date" class="input-field" />
              <input v-model="newCondition.doctor_clinic" class="input-field" placeholder="Doctor/Clinic" />
              <input v-model="newCondition.dietary_restrictions" class="input-field col-span-2" placeholder="Dietary restrictions" />
              <textarea v-model="newCondition.symptoms_to_monitor" class="input-field col-span-2" placeholder="Symptoms to monitor..."></textarea>
            </div>
            <div class="flex gap-2 mt-4">
              <button class="btn-primary" @click="onCreateCondition">Save</button>
              <button class="btn-tertiary" @click="resetConditionForm">Reset</button>
            </div>
          </div>
          
          <div v-if="conditions.length === 0 && !loading" class="text-center py-8 bg-white rounded-lg shadow">
            <p class="text-gray-500">You haven't added any conditions yet.</p>
          </div>
          <div v-else class="space-y-4">
            <div v-for="c in conditions" :key="c.condition_id" class="bg-white rounded-lg shadow p-4">
              <div class="flex items-center justify-between">
                <div class="flex-grow">
                  <h3 class="font-bold text-gray-800">{{ c.condition_name }}</h3>
                  <span class="text-xs px-2 py-0.5 rounded-full font-medium" :class="{
                    'bg-green-100 text-green-700': c.severity === 'mild',
                    'bg-yellow-100 text-yellow-700': c.severity === 'moderate',
                    'bg-red-100 text-red-700': c.severity === 'severe'
                  }">{{ c.severity }}</span>
                </div>
                <div class="flex gap-2">
                  <button class="text-xs text-blue-600 hover:underline" @click="selectCondition(c)">Add Meds</button>
                  <button class="text-xs text-red-600 hover:underline" @click="onDeleteCondition(c.condition_id)">Delete</button>
                </div>
              </div>
              <div class="text-sm text-gray-500 mt-2 space-y-1">
                <p v-if="c.diagnosed_date">Diagnosed: {{ formatDate(c.diagnosed_date) }}</p>
                <p v-if="c.doctor_clinic">Doctor: {{ c.doctor_clinic }}</p>
                <p v-if="c.dietary_restrictions">Restrictions: {{ c.dietary_restrictions }}</p>
                <p v-if="c.symptoms_to_monitor">Monitor: {{ c.symptoms_to_monitor }}</p>
              </div>
            </div>
          </div>
        </div>

        <div>
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-2xl font-bold text-gray-700">Medications</h2>
            <button class="btn-secondary" @click="showAddMedication = !showAddMedication">
              <span v-if="showAddMedication">Close</span>
              <span v-else>+ Add Medication</span>
            </button>
          </div>
          
          <div v-if="showAddMedication" class="bg-white rounded-lg shadow-sm p-4 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <select v-model="newMedication.condition_id" class="input-field col-span-2">
                <option disabled value="">Condition (optional)</option>
                <option v-for="c in conditions" :key="c.condition_id" :value="c.condition_id">{{ c.condition_name }}</option>
              </select>
              <input v-model="newMedication.medication_name" class="input-field" placeholder="Medication name" />
              <input v-model="newMedication.dosage" class="input-field" placeholder="Dosage" />
              <input v-model="newMedication.frequency" class="input-field" placeholder="Frequency" />
              <input v-model="newMedication.start_date" type="date" class="input-field" />
              <input v-model="newMedication.end_date" type="date" class="input-field" />
              <input v-model="newMedication.prescribing_doctor" class="input-field" placeholder="Prescribing doctor" />
              <textarea v-model="newMedication.instructions" class="input-field col-span-2" placeholder="Instructions..."></textarea>
            </div>
            <div class="flex gap-2 mt-4">
              <button class="btn-primary" @click="onCreateMedication">Save</button>
              <button class="btn-tertiary" @click="resetMedicationForm">Reset</button>
            </div>
          </div>
          
          <div v-if="medications.length === 0 && !loading" class="text-center py-8 bg-white rounded-lg shadow">
            <p class="text-gray-500">You haven't added any medications yet.</p>
          </div>
          <div v-else class="space-y-4">
            <div v-for="m in medications" :key="m.medication_id" class="bg-white rounded-lg shadow p-4">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-bold text-gray-800">{{ m.medication_name }}<span v-if="m.dosage" class="font-normal text-sm text-gray-600"> • {{ m.dosage }}</span></h3>
                  <div class="text-sm text-gray-500" v-if="m.frequency">Frequency: {{ m.frequency }}</div>
                </div>
                <div class="flex gap-2">
                  <button class="text-xs text-blue-700 hover:underline" @click="toggleLogs(m)">
                    {{ logsOpen[m.medication_id] ? 'Hide Logs' : 'Show Logs' }}
                  </button>
                  <button class="text-xs text-red-600 hover:underline" @click="onDeleteMedication(m.medication_id)">Delete</button>
                </div>
              </div>

              <div v-if="logsOpen[m.medication_id]" class="mt-4 pt-4 border-t border-gray-200">
                <div class="flex items-center justify-between mb-2">
                  <div class="font-semibold text-sm">Intake Logs</div>
                  <div class="text-xs text-gray-500" v-if="loadingLogs[m.medication_id]">Loading...</div>
                </div>
                
                <div v-if="(logsByMed[m.medication_id] || []).length === 0" class="text-xs text-gray-500">No logs yet.</div>
                <ul v-else class="space-y-1 text-xs text-gray-600">
                  <li v-for="log in logsByMed[m.medication_id]" :key="log.log_id" class="flex justify-between items-center bg-gray-50 rounded px-2 py-1">
                    <span>
                      <span class="font-medium">{{ log.quantity_taken || '—' }}</span>
                      <span class="ml-1">{{ formatDateTime(log.taken_at) }}</span>
                    </span>
                    <span v-if="log.notes" class="text-xs text-gray-400">Notes: {{ log.notes }}</span>
                  </li>
                </ul>

                <div class="mt-4 grid grid-cols-1 md:grid-cols-3 gap-2">
                  <input v-model="logForms[m.medication_id].quantity" class="input-field" placeholder="Quantity" />
                  <input v-model="logForms[m.medication_id].taken_at" type="datetime-local" class="input-field" />
                  <div class="col-span-1">
                    <button class="btn-primary w-full" @click="onCreateLog(m)">Add Log</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
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

const toasts = ref([])
function toast(message, type = 'success', duration = 2500) {
  const id = Date.now() + Math.random()
  toasts.value.push({ id, message, type })
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }, duration)
}

const showAddCondition = ref(false)
const showAddMedication = ref(false)
const selectedConditionId = ref('')

const logsOpen = ref({})
const logsByMed = ref({})
const loadingLogs = ref({})
const logForms = ref({})

function ensureLogForm(medId) {
  if (!logForms.value[medId]) {
    logForms.value = { ...logForms.value, [medId]: { quantity: '', notes: '', taken_at: '' } }
  }
}

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
  ensureLogForm(id)
  const isOpen = !!logsOpen.value[id]
  logsOpen.value = { ...logsOpen.value, [id]: !isOpen }
  if (!isOpen) {
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
    const logs = await getMedicationLogs(id)
    logsByMed.value = { ...logsByMed.value, [id]: logs }
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

<style scoped>
.input-field {
  @apply w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all text-sm;
}
.btn-primary {
  @apply bg-blue-600 text-white font-semibold px-4 py-2 rounded-lg shadow-md hover:bg-blue-700 transition-all text-sm;
}
.btn-secondary {
  @apply bg-white text-gray-800 font-semibold px-4 py-2 rounded-lg border border-gray-300 shadow-sm hover:bg-gray-100 transition-all text-sm;
}
.btn-tertiary {
  @apply bg-gray-200 text-gray-800 font-semibold px-4 py-2 rounded-lg hover:bg-gray-300 transition-all text-sm;
}
</style>