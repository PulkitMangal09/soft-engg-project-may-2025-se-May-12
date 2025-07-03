<template>
  <div class="flex flex-col min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="px-2 py-2 md:px-4 md:py-3 border-b border-gray-200 flex items-center justify-between bg-white">
      <button @click="$router.go(-1)" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100">
        ←
      </button>
      <h1 class="text-base md:text-lg font-semibold">Diet & Nutrition</h1>
      <button @click="showProfile = true"
        class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-500" fill="none" viewBox="0 0 24 24"
          stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
    </div>
    <!-- Main Content -->
    <div class="flex-1 overflow-y-auto p-2 md:p-4 space-y-4 md:space-y-6 max-w-5xl mx-auto w-full">
      <!-- Alert Banner -->
      <div
        class="bg-red-50 border border-red-200 border-l-4 border-l-red-500 rounded-xl p-3 md:p-4 animate-pulse mb-2 md:mb-4">
        <div class="font-semibold text-red-600 mb-1 flex items-center gap-1 text-sm md:text-base">⚠️ Nutrition Alert
        </div>
        <div class="text-xs md:text-sm text-red-900">Your sodium intake is 15% above recommended limit. Consider
          reducing salt in your next meal.</div>
      </div>
      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-2 md:gap-4 mb-2 md:mb-4">
        <div class="bg-white rounded-xl p-4 md:p-6 flex flex-col items-center shadow">
          <div class="text-lg md:text-xl font-bold text-emerald-500">1,842</div>
          <div class="text-xs text-gray-500">Calories Today</div>
          <div class="w-full h-2 bg-gray-200 rounded mt-2">
            <div class="h-2 bg-emerald-500 rounded" style="width: 75%"></div>
          </div>
        </div>
        <div class="bg-white rounded-xl p-4 md:p-6 flex flex-col items-center shadow">
          <div class="text-lg md:text-xl font-bold text-emerald-500">{{ waterCount }}/8</div>
          <div class="text-xs text-gray-500">Water Glasses</div>
          <div class="w-full h-2 bg-gray-200 rounded mt-2">
            <div class="h-2 bg-emerald-500 rounded" :style="`width: ${(waterCount / 8) * 100}%`"></div>
          </div>
        </div>
      </div>
      <!-- Water Tracker -->
      <div
        class="bg-blue-50 rounded-xl p-4 md:p-6 flex flex-col md:flex-row items-center justify-between mb-2 md:mb-4 gap-2 md:gap-0">
        <div class="mb-2 md:mb-0">
          <div class="font-bold">Daily Water Intake</div>
          <div class="text-xs text-gray-600">{{ waterCount }} of 8 glasses</div>
        </div>
        <div class="flex gap-1">
          <span v-for="i in 8" :key="i" class="inline-block w-4 h-6 rounded-b bg-white border-2 border-blue-400 mr-1"
            :class="{ 'bg-blue-400': i <= waterCount }"></span>
        </div>
      </div>
      <!-- Health Status Card -->
      <div class="bg-green-50 border-l-4 border-green-400 rounded-xl p-3 md:p-4 mb-2 md:mb-4">
        <div class="font-semibold text-green-700 mb-1 text-sm md:text-base">Health Status: Good</div>
        <div class="text-xs md:text-sm text-gray-700">BMI: 22.5 (Normal) • Weight: 65kg • Height: 170cm<br>Last updated:
          Today</div>
      </div>
      <!-- Nutrition Alert Card -->
      <div class="bg-orange-50 border-l-4 border-orange-400 rounded-xl p-3 md:p-4 mb-2 md:mb-4">
        <div class="font-semibold text-orange-700 mb-1 text-sm md:text-base">Nutrition Alert</div>
        <div class="text-xs md:text-sm text-orange-900">Your sugar intake is 15% above recommended daily limit. Consider
          reducing sweet snacks.</div>
      </div>
      <!-- Quick Actions -->
      <div class="bg-gray-50 rounded-xl p-4 md:p-6 mb-2 md:mb-4">
        <div class="font-semibold text-gray-800 mb-3 text-base md:text-lg">Quick Actions</div>
        <div class="grid grid-cols-3 gap-2 md:gap-3">
          <DietQuickActionCard icon="🍎" title="Log Food" @click="showLogFood = true" />
          <DietQuickActionCard icon="💧" title="Add Water" @click="addWater" />
          <DietQuickActionCard icon="⚖️" title="Log Weight" @click="showLogWeight = true" />
        </div>
      </div>
      <!-- Navigation Grid -->
      <div class="overflow-x-auto">
        <DietNavigationGrid />
      </div>
      <!-- Food Log -->
      <!-- Removed FoodLog from dashboard; now accessible via Food Log button in navigation grid -->
    </div>
    <!-- Log Food Modal -->
    <AppModal :show="showLogFood" title="Log Food" size="md" @close="showLogFood = false">
      <LogFoodForm :model-value="foodForm" @submit="submitFood; showLogFood = false" />
    </AppModal>
    <!-- Log Weight Modal -->
    <AppModal :show="showLogWeight" title="Log Weight" size="sm" @close="showLogWeight = false">
      <LogWeightForm @submit="submitWeight; showLogWeight = false" />
    </AppModal>
    <!-- Bottom Navigation -->
    <div
      class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 flex justify-around py-2 px-2 md:px-4 z-40 w-full">
      <router-link to="/student/tasks" :class="[
        'flex flex-col items-center py-1 px-2 rounded-lg transition-colors',
        $route.path.includes('/tasks') ? 'text-blue-600 bg-blue-50' : 'text-gray-500 hover:text-blue-500'
      ]">
        <span class="text-2xl">📋</span>
        <span class="text-xs mt-0.5">Tasks</span>
      </router-link>
      <router-link to="/student/finance" :class="[
        'flex flex-col items-center py-1 px-2 rounded-lg transition-colors',
        $route.path.includes('/finance') ? 'text-blue-600 bg-blue-50' : 'text-gray-500 hover:text-blue-500'
      ]">
        <span class="text-2xl">💰</span>
        <span class="text-xs mt-0.5">Finance</span>
      </router-link>
      <router-link to="/student/emotion" :class="[
        'flex flex-col items-center py-1 px-2 rounded-lg transition-colors',
        $route.path.includes('/emotion') ? 'text-blue-600 bg-blue-50' : 'text-gray-500 hover:text-blue-500'
      ]">
        <span class="text-2xl">😊</span>
        <span class="text-xs mt-0.5">Emotions</span>
      </router-link>
    </div>
    <!-- Profile Sidebar -->
    <ProfileSidebar v-if="showProfile" @close="showProfile = false" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import DietQuickActionCard from '@/components/diet/DietQuickActionCard.vue'
import DietStats from '@/components/diet/DietStats.vue'
import WaterTracker from '@/components/diet/WaterTracker.vue'
import FoodLog from '@/components/diet/FoodLog.vue'
import LogFoodForm from '@/components/diet/LogFoodForm.vue'
import LogWeightForm from '@/components/diet/LogWeightForm.vue'
import DietNavigationGrid from '@/components/diet/DietNavigationGrid.vue'
import ProfileSidebar from '@/components/profile/ProfileSidebar.vue'
import AppModal from '@/components/ui/AppModal.vue'

const showProfile = ref(false)
const waterCount = ref(6)
const showLogFood = ref(false)
const showLogWeight = ref(false)

function addWater() {
  if (waterCount.value < 8) waterCount.value++
}
function setWater(i) {
  waterCount.value = i
}

const meals = [
  {
    type: '🌅 Breakfast',
    icon: '🌅',
    totalCalories: 420,
    items: [
      { icon: '🥣', name: 'Oatmeal with Berries', quantity: '1 bowl', time: '8:30 AM', calories: 280 },
      { icon: '🥛', name: 'Milk (Low Fat)', quantity: '1 cup', time: '8:30 AM', calories: 140 },
    ]
  },
  {
    type: '🌞 Lunch',
    icon: '🌞',
    totalCalories: 580,
    items: [
      { icon: '🍗', name: 'Grilled Chicken Breast', quantity: '150g', time: '1:00 PM', calories: 350 },
      { icon: '🥗', name: 'Caesar Salad', quantity: '1 bowl', time: '1:00 PM', calories: 230 },
    ]
  },
  {
    type: '🍽️ Dinner',
    icon: '🍽️',
    totalCalories: 642,
    items: [
      { icon: '🍝', name: 'Spaghetti Marinara', quantity: '1 plate', time: '7:30 PM', calories: 480 },
      { icon: '🥖', name: 'Garlic Bread', quantity: '2 slices', time: '7:30 PM', calories: 162 },
    ]
  },
]

const foodForm = ref({
  mealType: 'Breakfast',
  foodName: '',
  quantity: 1,
  unit: 'Cup',
  time: '12:30',
  notes: ''
})

function submitFood(form) {
  // For now, just reset form
  foodForm.value = { mealType: 'Breakfast', foodName: '', quantity: 1, unit: 'Cup', time: '12:30', notes: '' }
}
function submitWeight(weight) {
  // For now, just log weight
  console.log('Weight submitted:', weight)
}
function scrollTo(id) {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
</script>

<style scoped>
.form-input,
.form-select,
.form-textarea {
  @apply border-2 border-gray-200 rounded-lg px-3 py-2 text-base focus:outline-none focus:border-indigo-500 w-full;
}

.btn-primary {
  @apply bg-gradient-to-r from-indigo-500 to-purple-500 text-white font-semibold rounded-lg py-2 px-4 mt-2 transition hover:shadow-lg;
}

.btn-secondary {
  @apply bg-white text-indigo-600 border-2 border-indigo-500 font-semibold rounded-lg py-2 px-4 mt-2 transition hover:bg-indigo-500 hover:text-white;
}

.add-btn {
  @apply bg-emerald-500 hover:bg-emerald-600 text-white rounded-full w-8 h-8 flex items-center justify-center;
}
</style>
