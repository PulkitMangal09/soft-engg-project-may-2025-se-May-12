<template>
  <div 
    class="flex flex-col items-center cursor-pointer"
    @click="$emit('click')"
  >
    <div class="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center text-2xl mb-1">
      {{ icon }}
    </div>
    <div class="text-xs text-center text-gray-700 font-medium">{{ title }}</div>
  </div>
</template>

<script setup>
defineProps({
  icon: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  }
});
</script>
