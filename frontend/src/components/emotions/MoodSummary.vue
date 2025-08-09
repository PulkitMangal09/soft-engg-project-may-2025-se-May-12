<template>
    <div class="bg-white rounded-xl p-4 shadow-sm">
        <h2 class="font-semibold text-gray-700 mb-3">Mood Summary</h2>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2">
            <div v-for="m in moods" :key="m.key" class="border rounded-lg p-3 flex flex-col items-center">
                <div class="text-2xl mb-1">{{ m.emoji }}</div>
                <div class="text-xs text-gray-500 capitalize">{{ m.key }}</div>
                <div class="text-lg font-semibold">{{ counts[m.key] || 0 }}</div>
            </div>
        </div>
        <div class="mt-4 grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div class="bg-blue-50 border border-blue-100 rounded-lg p-3">
                <div class="text-xs text-blue-700">Most frequent</div>
                <div class="text-sm font-semibold text-blue-800">{{ mostFrequentLabel }}</div>
            </div>
            <div class="bg-emerald-50 border border-emerald-100 rounded-lg p-3">
                <div class="text-xs text-emerald-700">Average stress</div>
                <div class="text-sm font-semibold text-emerald-800">{{ averageStress }}</div>
            </div>
            <div class="bg-amber-50 border border-amber-100 rounded-lg p-3">
                <div class="text-xs text-amber-700">Entries this week</div>
                <div class="text-sm font-semibold text-amber-800">{{ weeklyCount }}</div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    logs: { type: Array, default: () => [] }
})

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

const mostFrequentLabel = computed(() => {
    const c = counts.value
    let best = null
    let max = -1
    Object.keys(c).forEach(k => { if (c[k] > max) { max = c[k]; best = k } })
    return best ? `${best} (${max})` : '—'
})

const averageStress = computed(() => {
    const vals = (props.logs || [])
        .map(l => (l.stress_level || '').toLowerCase())
        .filter(Boolean)
        .map(v => v === 'high' ? 3 : v === 'moderate' ? 2 : 1)
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
