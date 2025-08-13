<template>
  <div class="min-h-screen bg-gray-100 flex flex-col items-center py-8 px-4">
        <button
      @click="$router.go(-1)"
      class="absolute top-4 left-4 w-10 h-10 flex items-center justify-center rounded-full bg-white text-gray-600 shadow-md hover:bg-gray-200 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-gray-300 transition-all z-10"
      aria-label="Go Back"
    >
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-6 h-6">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>
    <div class="w-full max-w-2xl">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800">Health Metrics Tracker 🩺</h1>
        <p class="text-gray-500 mt-2">Update your health data to monitor your progress.</p>
      </div>

      <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8">

        <h2 class="text-xl font-semibold text-gray-700 mb-4">Physical Details</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div class="input-group">
            <label class="input-label">Weight (kg)</label>
            <input type="number" class="input-field" :placeholder="placeholders.weight" v-model.number="form.weight" step="0.1" min="0">
          </div>
          <div class="input-group">
            <label class="input-label">Height (cm)</label>
            <input type="number" class="input-field" :placeholder="placeholders.height" v-model.number="form.height" step="0.5" min="0">
          </div>
          <div class="input-group">
            <label class="input-label">Age (years)</label>
            <input type="number" class="input-field" :placeholder="placeholders.age_years" v-model.number="form.age_years" min="0">
          </div>
          <div class="input-group">
            <label class="input-label">Sex</label>
            <template v-if="!isSexLocked">
              <select class="input-field" v-model="form.sex">
                <option value="" disabled>Select</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
              <div class="input-hint">This can only be set once.</div>
            </template>
            <template v-else>
              <div class="input-field bg-gray-100 cursor-not-allowed select-none">{{ placeholders.sex }}</div>
              <div class="input-hint">Locked (set previously)</div>
            </template>
          </div>
        </div>
        
        <div class="bg-green-50 border-2 border-green-200 rounded-xl p-5 text-center mb-6 shadow-sm">
          <div class="flex items-center justify-center mb-2">
            <span class="text-green-500 text-3xl mr-2">📊</span>
            <div class="font-bold text-lg text-gray-700">Calculated BMI</div>
          </div>
          <div class="text-5xl font-extrabold text-green-600 mb-1">{{ displayBmi }}</div>
          <div class="text-sm text-gray-600">Normal Weight Range</div>
        </div>

        <h2 class="text-xl font-semibold text-gray-700 mb-4">Health Vitals</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div class="input-group">
            <label class="input-label">Blood Pressure (mmHg)</label>
            <div class="flex gap-2">
              <input type="number" class="input-field" :placeholder="placeholders.systolic" v-model.number="form.systolic" min="0">
              <span class="flex items-center font-bold text-gray-500">/</span>
              <input type="number" class="input-field" :placeholder="placeholders.diastolic" v-model.number="form.diastolic" min="0">
            </div>
            <div class="input-hint">Systolic / Diastolic</div>
          </div>
          <div class="input-group">
            <label class="input-label">Blood Sugar (mg/dL)</label>
            <input type="number" class="input-field" :placeholder="placeholders.blood_sugar" v-model.number="form.blood_sugar" min="0">
            <div class="input-hint">Fasting: 70-100 | After meal: &lt;140</div>
          </div>
          <div class="input-group md:col-span-2">
            <label class="input-label">Heart Rate (bpm)</label>
            <input type="number" class="input-field" :placeholder="placeholders.heart_rate" v-model.number="form.heart_rate" min="0">
          </div>
          <div class="input-group md:col-span-2">
            <label class="input-label">Notes</label>
            <textarea class="input-field h-24" :placeholder="placeholders.notes || 'Any additional health notes...'" v-model="form.notes"></textarea>
          </div>
        </div>

        <div class="flex flex-col md:flex-row gap-4">
          <button class="btn-primary flex-1" :disabled="submitting || loading" @click="onSubmit">
            <span v-if="submitting">Saving...</span>
            <span v-else>Save Metrics</span>
          </button>
          <button class="btn-secondary flex-1">Set Reminder</button>
        </div>
      </div>
      <div class="text-center text-xs text-gray-400 mt-6">Health Metrics Update</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, getCurrentInstance } from 'vue'
import { useRouter } from 'vue-router'
import { getLatestMetrics, createMetrics } from '@/services/healthService'

const router = useRouter()
const { proxy } = getCurrentInstance()

const loading = ref(false)
const submitting = ref(false)

const placeholders = ref({
  weight: '',
  height: '',
  systolic: '',
  diastolic: '',
  blood_sugar: '',
  heart_rate: '',
  age_years: '',
  sex: '',
  notes: '',
  bmi: ''
})

const isSexLocked = computed(() => !!(placeholders.value.sex && placeholders.value.sex.length))

const form = ref({
  weight: null,
  height: null,
  systolic: null,
  diastolic: null,
  blood_sugar: null,
  heart_rate: null,
  age_years: null,
  sex: '',
  notes: ''
})

const bmiComputed = computed(() => {
  const w = Number(form.value.weight)
  const h = Number(form.value.height)
  if (!w || !h) return null
  const bmi = w / Math.pow(h / 100, 2)
  return Math.round(bmi * 10) / 10
})

const displayBmi = computed(() => {
  return bmiComputed.value ?? (placeholders.value.bmi || '—')
})

onMounted(async () => {
  loading.value = true
  try {
    const latest = await getLatestMetrics()
    placeholders.value = {
      weight: latest.weight?.toString?.() || '',
      height: latest.height?.toString?.() || '',
      systolic: latest.systolic?.toString?.() || '',
      diastolic: latest.diastolic?.toString?.() || '',
      blood_sugar: latest.blood_sugar?.toString?.() || '',
      heart_rate: latest.heart_rate?.toString?.() || '',
      age_years: latest.age_years?.toString?.() || '',
      sex: (latest.sex || '').trim(),
      notes: latest.notes || '',
      bmi: latest.bmi?.toString?.() || ''
    }
    if (placeholders.value.sex) {
      form.value.sex = placeholders.value.sex
    }
  } catch (e) {
    if (e?.response?.status && e.response.status !== 404) {
      proxy?.$toast?.error?.('Failed to load latest metrics')
    }
  } finally {
    loading.value = false
  }
})

function numOrPlaceholder(formVal, phVal) {
  const hasForm = formVal !== null && formVal !== undefined && formVal !== ''
  if (hasForm) return Number(formVal)
  if (phVal !== null && phVal !== undefined && phVal !== '') return Number(phVal)
  return null
}

function validate() {
  const w = numOrPlaceholder(form.value.weight, placeholders.value.weight)
  const h = numOrPlaceholder(form.value.height, placeholders.value.height)
  if (!w || !h) {
    proxy?.$toast?.error?.('Weight and Height are required (fill or rely on latest placeholders)')
    return false
  }
  if (!isSexLocked.value && !form.value.sex) {
    proxy?.$toast?.error?.('Please select Sex')
    return false
  }
  return true
}

async function onSubmit() {
  if (!validate()) return
  submitting.value = true
  try {
    const payload = {
      weight: numOrPlaceholder(form.value.weight, placeholders.value.weight) ?? 0,
      height: numOrPlaceholder(form.value.height, placeholders.value.height) ?? 0,
      systolic: numOrPlaceholder(form.value.systolic, placeholders.value.systolic) ?? 0,
      diastolic: numOrPlaceholder(form.value.diastolic, placeholders.value.diastolic) ?? 0,
      blood_sugar: numOrPlaceholder(form.value.blood_sugar, placeholders.value.blood_sugar) ?? 0,
      heart_rate: numOrPlaceholder(form.value.heart_rate, placeholders.value.heart_rate) ?? 0,
      age_years: numOrPlaceholder(form.value.age_years, placeholders.value.age_years),
      sex: ((placeholders.value.sex || form.value.sex || '').trim() || null),
      notes: form.value.notes || placeholders.value.notes || null
    }
    
    await createMetrics(payload)
    proxy?.$toast?.success?.('Health metrics saved')
    router.push('/student/health')
  } catch (e) {
    proxy?.$toast?.error?.('Failed to save metrics')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.input-group {
  @apply relative;
}

.input-label {
  @apply block font-semibold text-gray-700 mb-1 text-sm;
}

.input-field {
  @apply w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all;
}

.input-field::placeholder {
  @apply text-gray-400;
}

.input-field:focus {
  @apply border-blue-500;
}

.input-field.select-none {
  @apply appearance-none;
}

.input-hint {
  @apply text-xs text-gray-500 mt-1;
}

.btn-primary {
  @apply bg-blue-600 text-white font-semibold py-3 px-6 rounded-lg shadow-md hover:bg-blue-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed;
}

.btn-secondary {
  @apply bg-gray-200 text-gray-800 font-semibold py-3 px-6 rounded-lg shadow-md hover:bg-gray-300 transition-all;
}
</style>