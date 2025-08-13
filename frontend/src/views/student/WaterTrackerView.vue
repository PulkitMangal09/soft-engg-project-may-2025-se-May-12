<template>
  <div class="min-h-screen bg-gradient-to-b from-blue-50 to-white flex flex-col items-center py-8 px-4">
              <!-- 🔙 Go Back Button -->
    <button
      @click="$router.go(-1)"
      class="absolute top-4 left-4 w-10 h-10 flex items-center justify-center rounded-full bg-blue-100 text-blue-600 shadow hover:bg-blue-200 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-300 transition-all"
      aria-label="Go Back"
    >
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-5 h-5">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>
    <!-- Header Icon -->
    <div class="text-5xl mb-3">💧</div>

    <!-- Stats -->
    <div class="text-3xl font-semibold text-blue-700 mb-1">
      {{ glasses }} / 8 Glasses
    </div>
    <div class="text-sm text-gray-600 mb-6">Total: {{ totalMl }} ml</div>

    <!-- Main Card -->
    <div class="bg-white rounded-2xl shadow-xl w-full max-w-md p-6 flex flex-col items-center space-y-5">

      <!-- Glasses Visual -->
      <div class="flex justify-center gap-1">
        <span
          v-for="i in 8"
          :key="i"
          class="w-6 h-8 rounded-b-lg border-2"
          :class="i <= glasses ? 'bg-blue-400 border-blue-500' : 'bg-white border-blue-300'"
        ></span>
      </div>

      <!-- Quick Add Buttons -->
      <div class="grid grid-cols-3 gap-3 w-full">
        <button @click="quickAdd(250)" class="quick-btn">
          🥤<span class="text-xs">250ml</span>
        </button>
        <button @click="quickAdd(500)" class="quick-btn">
          🍶<span class="text-xs">500ml</span>
        </button>
        <button @click="quickAdd(200)" class="quick-btn">
          ☕<span class="text-xs">200ml</span>
        </button>
      </div>

      <!-- Hydration Log -->
      <div class="w-full bg-gray-50 rounded-lg p-4">
        <div class="font-semibold text-sm mb-2 text-blue-700">Today’s Hydration Log</div>
        <div class="text-xs text-gray-700 space-y-1 max-h-40 overflow-y-auto">
          <div
            v-for="l in logs"
            :key="l.intake_id"
            class="flex justify-between items-center border-b last:border-none pb-1"
          >
            <span class="font-mono">{{ formatTime(l.intake_time) }}</span>
            <span>{{ l.amount_ml }}ml ({{ l.container_type }})</span>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <button @click="customAdd" class="btn-primary w-full">Add Custom Amount</button>
      <button @click="refresh" class="btn-secondary w-full">Refresh</button>
    </div>

    <!-- Footer -->
    <div class="text-xs text-gray-400 mt-6">💧 Water Intake Tracker</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getWaterSummary, addWater, getWaterLogs } from '@/services/waterService'

const glasses = ref(0)
const totalMl = ref(0)
const logs = ref([])

function formatTime(t) {
  if (!t) return ''
  return t.slice(0, 5)
}

async function refresh() {
  const s = await getWaterSummary()
  totalMl.value = s.total_ml || 0
  glasses.value = Math.min(8, Math.round(totalMl.value / 250))
  logs.value = await getWaterLogs()
}

async function quickAdd(ml) {
  await addWater(ml, ml >= 500 ? 'bottle' : ml >= 250 ? 'glass' : 'cup')
  await refresh()
}

async function customAdd() {
  const ml = parseInt(prompt('Enter amount (ml):') || '0', 10)
  if (ml > 0) {
    await addWater(ml, ml >= 500 ? 'bottle' : ml >= 250 ? 'glass' : 'cup')
    await refresh()
  }
}

onMounted(refresh)
</script>

<style scoped>
.quick-btn {
  @apply flex flex-col items-center justify-center bg-blue-50 hover:bg-blue-100 text-blue-600 font-medium py-2 rounded-lg transition;
}

.btn-primary {
  @apply bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition;
}

.btn-secondary {
  @apply border border-blue-300 text-blue-600 hover:bg-blue-50 font-semibold py-2 px-4 rounded-lg transition;
}
</style>
