<template>
  <button
    @click="$emit('click')"
    :aria-label="title"
    class="relative overflow-hidden rounded-2xl p-4 flex flex-col items-start gap-2 text-left shadow-sm hover:shadow-md transition transform hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-indigo-300"
    :class="bgClass"
  >
    <div class="flex items-center justify-between w-full">
      <div class="flex items-center gap-3">
        <div class="w-12 h-12 rounded-xl bg-white/70 flex items-center justify-center text-2xl">
          {{ icon }}
        </div>
        <div>
          <div class="font-semibold text-slate-800 leading-tight">{{ title }}</div>
          <div class="text-xs text-slate-500 mt-0.5">{{ subtitle }}</div>
        </div>
      </div>
      <div class="text-xs text-slate-400">→</div>
    </div>

    <!-- subtle decorative ellipse -->
    <div class="absolute -right-6 -top-8 w-36 h-36 rounded-full opacity-10 pointer-events-none" :style="{ background: ellipse }"></div>
  </button>
</template>

<script setup>
const props = defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  icon: { type: String, default: '🔆' },
  color: { type: String, default: 'from-indigo-50 to-indigo-100' }
})
const bgClass = `bg-gradient-to-br ${props.color}`
const ellipse = 'linear-gradient(135deg, rgba(255,255,255,0.8), rgba(255,255,255,0.2))'
</script>
