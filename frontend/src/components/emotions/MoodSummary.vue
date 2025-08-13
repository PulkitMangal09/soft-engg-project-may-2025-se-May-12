<template>
  <div class="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
    <div class="flex items-center justify-between mb-4">
      <h3 class="font-bold text-slate-800 text-lg flex items-center gap-2">📊 Mood Summary</h3>
      <div class="text-sm text-slate-500">Last 7 days</div>
    </div>

    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4">
      <div v-for="m in moods" :key="m.key" class="bg-gradient-to-b from-white to-gray-50 rounded-xl p-4 flex flex-col items-center gap-2 border border-gray-100">
        <div class="text-4xl">{{ m.emoji }}</div>
        <div class="text-sm text-slate-600 capitalize">{{ m.key }}</div>
        <div class="text-lg font-bold text-slate-800">{{ counts[m.key] || 0 }}</div>

        <!-- small progress indicator (if any) -->
        <div class="w-full mt-2">
          <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
            <div :style="{ width: progressPercent(m.key) + '%' }" class="h-2 rounded-full" :class="progressColor(m.key)"></div>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-5 grid grid-cols-1 sm:grid-cols-3 gap-3">
      <div class="rounded-xl p-3 bg-indigo-50 border border-indigo-100">
        <div class="text-xs uppercase text-indigo-700 font-medium">Most Frequent</div>
        <div class="font-semibold text-indigo-900 mt-1">{{ mostFrequentLabel }}</div>
      </div>
      <div class="rounded-xl p-3 bg-emerald-50 border border-emerald-100">
        <div class="text-xs uppercase text-emerald-700 font-medium">Average Stress</div>
        <div class="font-semibold text-emerald-900 mt-1">{{ averageStress }}</div>
      </div>
      <div class="rounded-xl p-3 bg-yellow-50 border border-yellow-100">
        <div class="text-xs uppercase text-yellow-700 font-medium">Entries This Week</div>
        <div class="font-semibold text-yellow-900 mt-1">{{ weeklyCount }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ logs: { type: Array, default: () => [] } })

const moods = [
  { key: 'happy', emoji: '😊' },
  { key: 'sad', emoji: '😢' },
  { key: 'angry', emoji: '😠' },
  { key: 'neutral', emoji: '😐' },
  { key: 'anxious', emoji: '😰' },
  { key: 'excited', emoji: '🎉' }
]

const counts = computed(() => {
  const map = {}
  for (const l of props.logs || []) {
    const k = (l.mood || 'neutral').toLowerCase()
    map[k] = (map[k] || 0) + 1
  }
  return map
})

const total = computed(() => Object.values(counts.value).reduce((a, b) => a + b, 0) || 0)

const progressPercent = (key) => {
  if (!total.value) return 0
  return Math.round(((counts.value[key] || 0) / total.value) * 100)
}
const progressColor = (key) => {
  const map = {
    happy: 'bg-green-400',
    sad: 'bg-blue-400',
    angry: 'bg-red-400',
    neutral: 'bg-yellow-400',
    anxious: 'bg-purple-400',
    excited: 'bg-pink-400'
  }
  return map[key] || 'bg-gray-300'
}

const mostFrequentLabel = computed(() => {
  const c = counts.value
  let best = null
  let max = -1
  Object.keys(c).forEach(k => { if (c[k] > max) { max = c[k]; best = k } })
  return best ? `${best} (${max})` : '—'
})

const averageStress = computed(() => {
  const vals = (props.logs || []).map(l => (l.stress_level || '').toLowerCase()).filter(Boolean).map(v => v === 'high' ? 3 : v === 'moderate' ? 2 : 1)
  if (!vals.length) return '—'
  const avg = vals.reduce((a, b) => a + b, 0) / vals.length
  return avg >= 2.5 ? 'High' : avg >= 1.5 ? 'Moderate' : 'Relaxed'
})

const weeklyCount = computed(() => {
  const now = new Date()
  const weekAgo = new Date(now)
  weekAgo.setDate(now.getDate() - 7)
  return (props.logs || []).filter(l => {
    const d = new Date(l.log_date || l.created_at)
    return d >= weekAgo && d <= now
  }).length
})
</script>
