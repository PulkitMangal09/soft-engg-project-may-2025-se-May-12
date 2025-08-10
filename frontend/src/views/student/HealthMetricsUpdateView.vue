<template>
    <div class="min-h-screen bg-gray-50 flex flex-col items-center py-6 px-2 md:px-0">
        <div class="bg-white rounded-xl shadow p-6 w-full max-w-md mb-4">
            <div class="mb-4">
                <label class="block font-semibold mb-1">Weight (kg)</label>
                <input type="number" class="form-input w-full mb-3" :placeholder="placeholders.weight" v-model.number="form.weight" step="0.1" min="0">
                <label class="block font-semibold mb-1">Height (cm)</label>
                <input type="number" class="form-input w-full mb-3" :placeholder="placeholders.height" v-model.number="form.height" step="0.5" min="0">
            </div>
            <div class="bg-green-50 border-l-4 border-green-400 rounded-lg p-4 mb-4">
                <div class="font-semibold mb-2">Calculated BMI</div>
                <div class="text-2xl font-bold text-green-600 mb-1">{{ displayBmi }}</div>
                <div class="text-sm text-gray-700">Normal Weight Range</div>
            </div>
            <div class="mb-4">
                <label class="block font-semibold mb-1">Blood Pressure</label>
                <div class="flex gap-2 mb-1">
                    <input type="number" class="form-input w-1/2" :placeholder="placeholders.systolic" v-model.number="form.systolic" min="0">
                    <span class="flex items-center font-bold">/</span>
                    <input type="number" class="form-input w-1/2" :placeholder="placeholders.diastolic" v-model.number="form.diastolic" min="0">
                </div>
                <div class="text-[10px] text-gray-500 mb-2">Systolic / Diastolic (mmHg)</div>
                <label class="block font-semibold mb-1">Blood Sugar (mg/dL)</label>
                <input type="number" class="form-input w-full mb-1" :placeholder="placeholders.blood_sugar" v-model.number="form.blood_sugar" min="0">
                <div class="text-[10px] text-gray-500 mb-2">Fasting: 70-100 | After meal: &lt;140</div>
                <label class="block font-semibold mb-1">Heart Rate (bpm)</label>
                <input type="number" class="form-input w-full mb-3" :placeholder="placeholders.heart_rate" v-model.number="form.heart_rate" min="0">
                <label class="block font-semibold mb-1">Notes</label>
                <textarea class="form-textarea w-full mb-3" :placeholder="placeholders.notes || 'Any additional health notes...'" v-model="form.notes"></textarea>
            </div>
            <button class="btn-primary w-full mb-2" :disabled="submitting || loading" @click="onSubmit">
              {{ submitting ? 'Saving...' : 'Save Metrics' }}
            </button>
            <!-- <button class="btn-secondary w-full">Set Reminder</button> -->
        </div>
        <div class="text-xs text-gray-400 mt-4">Health Metrics Update</div>
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
  notes: '',
  bmi: ''
})

const form = ref({
  weight: null,
  height: null,
  systolic: null,
  diastolic: null,
  blood_sugar: null,
  heart_rate: null,
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
      notes: latest.notes || '',
      bmi: latest.bmi?.toString?.() || ''
    }
  } catch (e) {
    // If 404, ignore; else show error
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