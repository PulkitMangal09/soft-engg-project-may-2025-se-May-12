<template>
  <div class="h-40 relative">
    <div class="absolute bottom-0 w-full flex justify-between items-end h-32 px-1">
      <div 
        v-for="(day, index) in moodData" 
        :key="index"
        class="flex-1 flex flex-col items-center"
      >
        <div 
          class="w-4 rounded-t-sm"
          :class="getMoodColor(day.mood)"
          :style="{ height: `${day.value * 16}px` }"
        ></div>
        <span class="text-xs text-gray-500 mt-1">{{ day.day }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
const moodData = [
  { day: 'M', mood: 'happy', value: 4 },
  { day: 'T', mood: 'sad', value: 2 },
  { day: 'W', mood: 'angry', value: 1 },
  { day: 'T', mood: 'neutral', value: 3 },
  { day: 'F', mood: 'happy', value: 4 },
  { day: 'S', mood: 'happy', value: 5 },
  { day: 'S', mood: 'sad', value: 2 },
];

const getMoodColor = (mood) => {
  const colors = {
    happy: 'bg-green-500',
    sad: 'bg-blue-500',
    angry: 'bg-red-500',
    neutral: 'bg-yellow-500',
  };
  return colors[mood] || 'bg-gray-200';
};
</script>
