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

        <div class="w-full max-w-4xl">
            <header class="text-center mb-8">
                <h1 class="text-4xl font-bold text-gray-800">Nutrition Suggestions 🥗</h1>
                <p class="mt-2 text-gray-500">Insights and advice based on your health data.</p>
            </header>

            <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8">
                <div class="flex flex-col md:flex-row md:items-end md:justify-between gap-4 mb-6 border-b pb-6">
                    <div class="flex-1">
                        <label for="range-select" class="block text-sm font-medium text-gray-700 mb-1">Select Range</label>
                        <select id="range-select" v-model="range" class="input-field w-full">
                            <option value="today">Today</option>
                            <option value="7d">Last 7 days</option>
                            <option value="30d">Last 30 days</option>
                        </select>
                    </div>
                    <div class="flex gap-3">
                        <button class="btn-secondary" :disabled="loading" @click="refreshLatest">Refresh</button>
                        <button class="btn-primary" :disabled="loading" @click="onGenerate">
                            {{ loading ? 'Generating…' : 'Generate Suggestions' }}
                        </button>
                    </div>
                </div>

                <div v-if="loading" class="text-center text-gray-500 py-10">
                    <div class="spinner-border animate-spin inline-block w-8 h-8 border-4 rounded-full" role="status"></div>
                    <p class="mt-3">Generating personalized suggestions...</p>
                </div>
                
                <div v-else-if="error" class="bg-red-100 border-l-4 border-red-500 rounded-lg p-4 text-sm text-red-800 mb-4">
                    <p class="font-semibold">Error:</p>
                    <p>{{ error }}</p>
                </div>

                <div v-else-if="!suggestions" class="text-center text-gray-600 py-10">
                    <p>No suggestions found for this range. Click "Generate Suggestions" to get started.</p>
                </div>

                <div v-else class="space-y-6">
                    <div class="bg-green-50 border-l-4 border-green-400 rounded-lg p-4 shadow-sm">
                        <h3 class="font-semibold text-lg flex items-center gap-2 mb-1 text-green-800">
                           <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                            </svg>
                            Overview
                        </h3>
                        <p class="text-sm text-gray-800">{{ suggestions.overview }}</p>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="bg-white border rounded-lg p-4 shadow-sm">
                            <h3 class="font-semibold text-gray-800 mb-2 flex items-center gap-2">
                                <span class="text-indigo-500">🎯</span> Macro Targets
                            </h3>
                            <div class="text-sm text-gray-700 space-y-1">
                                <div>Calories: <span class="font-semibold">{{ n(suggestions.macro_targets?.calories) }}</span></div>
                                <div>Proteins (g): <span class="font-semibold">{{ n(suggestions.macro_targets?.proteins) }}</span></div>
                                <div>Carbs (g): <span class="font-semibold">{{ n(suggestions.macro_targets?.carbs) }}</span></div>
                                <div>Fat (g): <span class="font-semibold">{{ n(suggestions.macro_targets?.fat) }}</span></div>
                                <div v-if="suggestions.macro_targets?.sodium !== undefined">Sodium (mg): <span class="font-semibold">{{ n(suggestions.macro_targets?.sodium) }}</span></div>
                                <div v-if="suggestions.macro_targets?.sugar !== undefined">Sugar (g): <span class="font-semibold">{{ n(suggestions.macro_targets?.sugar) }}</span></div>
                            </div>
                        </div>
                        
                        <div class="bg-white border rounded-lg p-4 shadow-sm">
                            <h3 class="font-semibold text-gray-800 mb-2 flex items-center gap-2">
                                <span class="text-blue-500">💧</span> Hydration Advice
                            </h3>
                            <p class="text-sm text-gray-700">{{ suggestions.hydration_advice || '—' }}</p>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="bg-orange-50 border-l-4 border-orange-400 rounded-lg p-4 shadow-sm">
                            <h3 class="font-semibold text-lg mb-1 flex items-center gap-2 text-orange-800">
                                <span class="text-orange-500">⚠️</span> Risks
                            </h3>
                            <ul class="list-disc list-inside text-sm text-gray-800">
                                <li v-for="(r, idx) in (suggestions.risks || [])" :key="idx">{{ r }}</li>
                                <li v-if="!suggestions.risks || suggestions.risks.length === 0" class="text-gray-500">None</li>
                            </ul>
                        </div>
                        <div class="bg-red-50 border-l-4 border-red-400 rounded-lg p-4 shadow-sm">
                            <h3 class="font-semibold text-lg mb-1 flex items-center gap-2 text-red-800">
                                <span class="text-red-500">🚨</span> Alerts
                            </h3>
                            <ul class="list-disc list-inside text-sm text-gray-800">
                                <li v-for="(a, idx) in (suggestions.alerts || [])" :key="idx">{{ a }}</li>
                                <li v-if="!suggestions.alerts || suggestions.alerts.length === 0" class="text-gray-500">None</li>
                            </ul>
                        </div>
                    </div>

                    <div class="bg-white border rounded-lg p-4 shadow-sm">
                        <h3 class="font-semibold text-lg mb-4 flex items-center gap-2 text-gray-800">
                            <span class="text-green-500">🍽️</span> Meal Plan
                        </h3>
                        <div class="space-y-3">
                            <div v-for="(m, idx) in (suggestions.meal_plan || [])" :key="idx" class="p-3 rounded-lg bg-gray-50 border border-gray-200">
                                <div class="text-xs text-gray-500 mb-1 font-medium">{{ m.timeOfDay || 'Meal' }}</div>
                                <div class="font-semibold text-gray-800">{{ m.item }}</div>
                                <div class="text-sm text-gray-600 mt-1">{{ m.rationale }}</div>
                            </div>
                            <div v-if="!suggestions.meal_plan || suggestions.meal_plan.length === 0" class="text-sm text-gray-500 text-center">No meal plan suggestions available.</div>
                        </div>
                    </div>

                    <div v-if="suggestions.notes" class="bg-white border rounded-lg p-4 shadow-sm">
                        <h3 class="font-semibold text-lg mb-1 text-gray-800">Notes</h3>
                        <p class="text-sm text-gray-700">{{ suggestions.notes }}</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="text-xs text-gray-400 mt-6">Nutrition Suggestions powered by AI</div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { generateSuggestions, getLatestSuggestions } from '@/services/nutritionService'

const range = ref('today')
const loading = ref(false)
const error = ref('')
const suggestions = ref(null)

function n(v) {
  const num = Number(v)
  return isFinite(num) ? (Math.round(num * 10) / 10) : 0
}

async function refreshLatest() {
  error.value = ''
  try {
    const res = await getLatestSuggestions(range.value)
    suggestions.value = res?.suggestions || null
    if (!suggestions.value) {
      error.value = 'No saved suggestions found for this range.'
    }
  } catch (e) {
    suggestions.value = null
    error.value = 'No saved suggestions found for this range.'
  }
}

async function onGenerate() {
  loading.value = true
  error.value = ''
  try {
    const res = await generateSuggestions(range.value)
    suggestions.value = res?.suggestions || null
  } catch (e) {
    error.value = 'Failed to generate suggestions. Please try again.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  refreshLatest()
})
</script>

<style scoped>
.input-field {
  @apply border-2 border-gray-200 rounded-lg px-4 py-2 text-base focus:outline-none focus:border-indigo-500 transition-colors;
}

.btn-primary {
  @apply bg-emerald-500 hover:bg-emerald-600 text-white font-semibold rounded-lg py-2 px-6 transition-colors disabled:opacity-60 disabled:cursor-not-allowed;
}

.btn-secondary {
  @apply bg-white text-emerald-600 border-2 border-emerald-500 font-semibold rounded-lg py-2 px-6 hover:bg-emerald-50 transition-colors disabled:opacity-60 disabled:cursor-not-allowed;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.spinner-border {
  animation: spin 1s linear infinite;
  border-color: currentColor;
  border-right-color: transparent;
}
</style>