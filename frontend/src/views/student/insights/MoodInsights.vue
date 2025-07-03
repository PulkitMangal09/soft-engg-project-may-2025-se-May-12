<template>
  <div class="p-4 max-w-4xl mx-auto">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Mood Insights</h1>
      <div class="text-sm text-gray-500">
        <select v-model="selectedPeriod" class="bg-white border border-gray-300 rounded-md px-3 py-1 text-sm">
          <option value="week">This Week</option>
          <option value="month">This Month</option>
          <option value="year">This Year</option>
        </select>
      </div>
    </div>

    <!-- Mood Summary Card -->
    <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">Your Mood Overview</h2>
      <div class="flex items-center justify-between mb-6">
        <div class="text-center">
          <div class="text-4xl">😊</div>
          <div class="text-sm text-gray-600">Most Common</div>
          <div class="font-medium">Happy</div>
        </div>
        <div class="text-center">
          <div class="text-4xl">😔</div>
          <div class="text-sm text-gray-600">Recent</div>
          <div class="font-medium">Sad</div>
        </div>
        <div class="text-center">
          <div class="text-4xl">📈</div>
          <div class="text-sm text-gray-600">Trend</div>
          <div class="font-medium text-green-500">+12%</div>
        </div>
      </div>
    </div>

    <!-- Mood Chart -->
    <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">Mood Over Time</h2>
      <div class="h-64 flex items-end justify-between pt-8">
        <div v-for="(day, index) in moodData" :key="index" class="flex flex-col items-center">
          <div 
            class="w-8 bg-blue-100 rounded-t-sm" 
            :style="{ height: day.height + 'px', backgroundColor: day.color }"
          ></div>
          <div class="text-xs mt-2 text-gray-500">{{ day.day }}</div>
        </div>
      </div>
    </div>

    <!-- Mood Triggers -->
    <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">Common Triggers</h2>
      <div class="space-y-3">
        <div v-for="(trigger, index) in commonTriggers" :key="index" class="flex items-center">
          <div class="w-3/5 text-sm text-gray-600">{{ trigger.name }}</div>
          <div class="w-2/5">
            <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
              <div 
                class="h-full bg-blue-500 rounded-full" 
                :style="{ width: trigger.percentage + '%' }"
              ></div>
            </div>
          </div>
          <div class="w-10 text-right text-xs text-gray-500">{{ trigger.percentage }}%</div>
        </div>
      </div>
    </div>

    <!-- Mood Tips -->
    <div class="bg-blue-50 rounded-xl p-6">
      <h2 class="text-lg font-semibold text-blue-800 mb-2">Mood Improvement Tips</h2>
      <p class="text-blue-700 text-sm mb-4">Based on your recent entries, here are some suggestions:</p>
      <ul class="space-y-2 text-sm text-blue-800">
        <li class="flex items-start">
          <span class="mr-2">•</span>
          <span>Try deep breathing exercises when feeling anxious</span>
        </li>
        <li class="flex items-start">
          <span class="mr-2">•</span>
          <span>Reach out to friends when feeling down</span>
        </li>
        <li class="flex items-start">
          <span class="mr-2">•</span>
          <span>Take regular breaks during study sessions</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const selectedPeriod = ref('week');

const moodData = [
  { day: 'Mon', mood: 'happy', height: 60, color: '#4F46E5' },
  { day: 'Tue', mood: 'sad', height: 30, color: '#4F46E5' },
  { day: 'Wed', mood: 'neutral', height: 45, color: '#4F46E5' },
  { day: 'Thu', mood: 'happy', height: 65, color: '#4F46E5' },
  { day: 'Fri', mood: 'excited', height: 80, color: '#4F46E5' },
  { day: 'Sat', mood: 'sad', height: 35, color: '#4F46E5' },
  { day: 'Sun', mood: 'happy', height: 70, color: '#4F46E5' },
];

const commonTriggers = [
  { name: 'School Work', percentage: 65 },
  { name: 'Social Interactions', percentage: 45 },
  { name: 'Family', percentage: 30 },
  { name: 'Health', percentage: 25 },
];

// Watch for period changes to fetch new data
watch(selectedPeriod, (newPeriod) => {
  console.log('Fetching data for period:', newPeriod);
  // In a real app, you would fetch data based on the selected period
});
</script>

<style scoped>
/* Add any custom styles here */
</style>
