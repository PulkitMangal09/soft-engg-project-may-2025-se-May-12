<template>
    <div class="min-h-screen bg-gray-50 flex flex-col items-center py-6 px-2 md:px-0">
        <div class="bg-white rounded-xl shadow p-4 md:p-6 w-full max-w-2xl mb-4">
            <div class="flex flex-col md:flex-row md:items-end gap-3 md:gap-4 mb-4">
                <div class="flex-1">
                    <div class="text-sm text-gray-700 mb-1">Range</div>
                    <select v-model="range" class="border-2 border-gray-200 rounded-lg px-3 py-2 text-base focus:outline-none focus:border-indigo-500 w-full">
                        <option value="today">Today</option>
                        <option value="7d">Last 7 days</option>
                        <option value="30d">Last 30 days</option>
                    </select>
                </div>
                <div class="flex gap-2">
                    <button class="bg-white text-emerald-600 border-2 border-emerald-500 font-semibold rounded-lg py-2 px-4 hover:bg-emerald-50 disabled:opacity-60" :disabled="loading" @click="refreshLatest">Refresh</button>
                    <button class="bg-emerald-500 hover:bg-emerald-600 text-white font-semibold rounded-lg py-2 px-4 disabled:opacity-60" :disabled="loading" @click="onGenerate">
                        {{ loading ? 'Generating…' : 'Generate Suggestions' }}
                    </button>
                </div>
            </div>

            <div v-if="error" class="bg-red-50 border-l-4 border-red-500 rounded-lg p-3 text-sm text-red-800 mb-4">
                {{ error }}
            </div>

            <div v-if="!suggestions && !loading" class="text-sm text-gray-600">
                No suggestions yet for this range. Click "Generate Suggestions".
            </div>

            <div v-if="suggestions" class="space-y-4">
                <div class="bg-green-50 border-l-4 border-green-400 rounded-lg p-4">
                    <div class="font-semibold mb-1">Overview</div>
                    <div class="text-sm text-gray-800">{{ suggestions.overview }}</div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div class="bg-white border rounded-lg p-4">
                        <div class="font-semibold text-gray-800 mb-2">Macro Targets</div>
                        <div class="text-sm text-gray-700 space-y-1">
                            <div>Calories: <span class="font-semibold">{{ n(suggestions.macro_targets?.calories) }}</span></div>
                            <div>Proteins (g): <span class="font-semibold">{{ n(suggestions.macro_targets?.proteins) }}</span></div>
                            <div>Carbs (g): <span class="font-semibold">{{ n(suggestions.macro_targets?.carbs) }}</span></div>
                            <div>Fat (g): <span class="font-semibold">{{ n(suggestions.macro_targets?.fat) }}</span></div>
                            <div v-if="suggestions.macro_targets?.sodium !== undefined">Sodium (mg): <span class="font-semibold">{{ n(suggestions.macro_targets?.sodium) }}</span></div>
                            <div v-if="suggestions.macro_targets?.sugar !== undefined">Sugar (g): <span class="font-semibold">{{ n(suggestions.macro_targets?.sugar) }}</span></div>
                        </div>
                    </div>
                    <div class="bg-white border rounded-lg p-4">
                        <div class="font-semibold text-gray-800 mb-2">Hydration Advice</div>
                        <div class="text-sm text-gray-700">{{ suggestions.hydration_advice || '—' }}</div>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div class="bg-orange-50 border-l-4 border-orange-400 rounded-lg p-4">
                        <div class="font-semibold mb-1">Risks</div>
                        <ul class="list-disc list-inside text-sm text-gray-800">
                            <li v-for="(r, idx) in (suggestions.risks || [])" :key="idx">{{ r }}</li>
                            <li v-if="!suggestions.risks || suggestions.risks.length === 0" class="text-gray-500">None</li>
                        </ul>
                    </div>
                    <div class="bg-red-50 border-l-4 border-red-400 rounded-lg p-4">
                        <div class="font-semibold mb-1">Alerts</div>
                        <ul class="list-disc list-inside text-sm text-gray-800">
                            <li v-for="(a, idx) in (suggestions.alerts || [])" :key="idx">{{ a }}</li>
                            <li v-if="!suggestions.alerts || suggestions.alerts.length === 0" class="text-gray-500">None</li>
                        </ul>
                    </div>
                </div>

                <div class="bg-gray-50 border rounded-lg p-4">
                    <div class="font-semibold mb-2">Meal Plan</div>
                    <div class="space-y-2">
                        <div v-for="(m, idx) in (suggestions.meal_plan || [])" :key="idx" class="p-3 rounded bg-white border">
                            <div class="text-sm text-gray-500">{{ m.timeOfDay || 'Meal' }}</div>
                            <div class="font-semibold">{{ m.item }}</div>
                            <div class="text-xs text-gray-600">{{ m.rationale }}</div>
                        </div>
                        <div v-if="!suggestions.meal_plan || suggestions.meal_plan.length === 0" class="text-sm text-gray-500">No items</div>
                    </div>
                </div>

                <div v-if="suggestions.notes" class="bg-white border rounded-lg p-4">
                    <div class="font-semibold">Notes</div>
                    <div class="text-sm text-gray-700">{{ suggestions.notes }}</div>
                </div>
            </div>
        </div>
        <div class="text-xs text-gray-400 mt-2">Nutrition Suggestions</div>
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