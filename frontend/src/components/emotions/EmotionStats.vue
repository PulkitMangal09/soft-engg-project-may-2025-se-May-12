<template>
  <div class="bg-gradient-to-b from-white to-blue-50 rounded-2xl p-5 shadow-md border border-blue-100">
    <!-- Header + Legend -->
    <div class="flex flex-wrap items-center justify-between mb-5 gap-3">
      <h3 class="font-bold text-gray-800 text-lg flex items-center gap-2">
        📈 7-Day Mood Trends
      </h3>
      <div class="flex flex-wrap gap-2 text-xs">
        <span
          v-for="l in legend"
          :key="l.key"
          class="flex items-center gap-1 px-2 py-0.5 rounded-full border border-gray-200 bg-white shadow-sm"
        >
          <span :class="l.class" class="inline-block w-3 h-3 rounded-full"></span>
          <span class="capitalize font-medium">{{ l.label }}</span>
        </span>
      </div>
    </div>

    <!-- Chart -->
    <div class="h-44 relative">
      <div class="absolute bottom-0 w-full flex justify-between items-end h-36 px-1">
        <div
          v-for="(d, idx) in chartData"
          :key="idx"
          class="flex-1 flex flex-col items-center group"
        >
          <div
            class="w-6 rounded-t-full transition-all duration-300 ease-out group-hover:opacity-90 group-hover:scale-x-105 shadow-sm"
            :class="getMoodColor(d.mood)"
            :style="{ height: `${Math.max(8, d.count * 16)}px` }"
            :title="`${d.label}: ${d.count} entr${d.count === 1 ? 'y' : 'ies'}\nDominant: ${d.mood}`"
          ></div>
          <div class="text-2xl mt-2" aria-hidden="true">{{ moodEmoji(d.mood) }}</div>
          <span class="text-xs text-gray-500">{{ d.day }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { listMoodLogs } from '@/services/moodService'

const chartData = ref([])
const legend = [
  { key: 'happy', label: 'Happy', class: 'bg-green-400' },
  { key: 'sad', label: 'Sad', class: 'bg-blue-400' },
  { key: 'angry', label: 'Angry', class: 'bg-red-400' },
  { key: 'neutral', label: 'Neutral', class: 'bg-yellow-400' },
  { key: 'anxious', label: 'Anxious', class: 'bg-purple-400' },
  { key: 'excited', label: 'Excited', class: 'bg-pink-400' },
]

onMounted(async () => {
  const logs = await listMoodLogs()
  const byDate = new Map()
  for (const l of logs) {
    const dt = new Date(l.log_date || l.created_at)
    const key = dt.toISOString().slice(0, 10)
    if (!byDate.has(key)) byDate.set(key, [])
    byDate.get(key).push(l)
  }

  const out = []
  for (let i = 6; i >= 0; i--) {
    const d = new Date()
    d.setDate(d.getDate() - i)
    const key = d.toISOString().slice(0, 10)
    const arr = byDate.get(key) || []
    const counts = {}
    for (const a of arr) counts[a.mood] = (counts[a.mood] || 0) + 1
    const dominant = Object.keys(counts).sort((a, b) => counts[b] - counts[a])[0] || 'neutral'
    out.push({
      label: d.toLocaleDateString(),
      day: d.toLocaleDateString('en-US', { weekday: 'short' }).charAt(0),
      count: arr.length,
      mood: dominant
    })
  }
  chartData.value = out
})

const getMoodColor = (mood) => {
  const colors = {
    happy: 'bg-green-400',
    sad: 'bg-blue-400',
    angry: 'bg-red-400',
    neutral: 'bg-yellow-400',
    anxious: 'bg-purple-400',
    excited: 'bg-pink-400',
  }
  return colors[mood] || 'bg-gray-200'
}

function moodEmoji(mood) {
  const map = {
    happy: '😊',
    sad: '😢',
    angry: '😠',
    neutral: '😐',
    anxious: '😰',
    excited: '🎉'
  }
  return map[mood] || '🙂'
}
</script>
