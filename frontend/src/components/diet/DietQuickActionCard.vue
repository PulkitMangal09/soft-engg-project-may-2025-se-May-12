<template>
  <div
    class="flex flex-col items-center cursor-pointer p-4 rounded-xl transition-all duration-200 ease-in-out transform hover:-translate-y-1 hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
    @click="$emit('click')"
  >
    <div
      class="w-16 h-16 md:w-20 md:h-20 rounded-full flex items-center justify-center text-4xl mb-2 transition-all duration-200"
      :class="iconBgColor"
    >
      {{ icon }}
    </div>
    <div class="text-sm md:text-base text-center text-gray-800 font-semibold mt-1">
      {{ title }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  icon: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  }
});

// A computed property to assign a different background color based on the icon.
// This adds visual variety and is more engaging.
const iconBgColor = computed(() => {
  switch (props.icon) {
    case '🍎': return 'bg-red-100 text-red-600';
    case '💧': return 'bg-blue-100 text-blue-600';
    case '⚖️': return 'bg-yellow-100 text-yellow-600';
    default: return 'bg-gray-100 text-gray-600';
  }
});
</script>

<style scoped>
/* Optional: Add custom styles if needed, but Tailwind classes should be sufficient */
</style>