<template>
  <div class="bg-white rounded-xl p-4 shadow-sm">
    <div class="flex items-center justify-between mb-2">
      <h3 class="font-semibold text-gray-700">7-Day Trends</h3>
      <div class="flex gap-2 items-center text-xs">
        <span v-for="l in legend" :key="l.key" class="inline-flex items-center gap-1">
          <span :class="l.class" class="inline-block w-3 h-3 rounded-sm"></span>{{ l.label }}
        </span>
      </div>
    </div>
    <div class="h-40 relative">
      <div class="absolute bottom-0 w-full flex justify-between items-end h-32 px-1">
        <div v-for="(d, idx) in chartData" :key="idx" class="flex-1 flex flex-col items-center group">
          <div class="w-6 rounded-t-md transition-all duration-200 group-hover:opacity-90" :class="getMoodColor(d.mood)"
            :style="{ height: `${Math.max(6, d.count * 14)}px` }"
            :title="`${d.label}: ${d.count} entr${d.count === 1 ? 'y' : 'ies'}\nDominant: ${d.mood}`"></div>
          <div class="text-lg mt-1" aria-hidden="true">{{ moodEmoji(d.mood) }}</div>
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
  { key: 'happy', label: 'Happy', class: 'bg-green-500' },
  { key: 'sad', label: 'Sad', class: 'bg-blue-500' },
  { key: 'angry', label: 'Angry', class: 'bg-red-500' },
  { key: 'neutral', label: 'Neutral', class: 'bg-yellow-500' },
  { key: 'anxious', label: 'Anxious', class: 'bg-purple-500' },
  { key: 'excited', label: 'Excited', class: 'bg-pink-500' },
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
    happy: 'bg-green-500',
    sad: 'bg-blue-500',
    angry: 'bg-red-500',
    neutral: 'bg-yellow-500',
    anxious: 'bg-purple-500',
    excited: 'bg-pink-500',
  };
  return colors[mood] || 'bg-gray-200';
};

function moodEmoji(mood) {
  const map = { happy: '😊', sad: '😢', angry: '😠', neutral: '😐', anxious: '😰', excited: '🎉' }
  return map[mood] || '🙂'
}
</script>
