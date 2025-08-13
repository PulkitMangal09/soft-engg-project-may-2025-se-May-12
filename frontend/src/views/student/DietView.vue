<template>
  <div class="min-h-screen bg-gray-100 relative">
    <StudentNavBar />

    <button @click="$router.go(-1)" class="absolute top-4 left-4 z-10 w-10 h-10 flex items-center justify-center rounded-full bg-white text-gray-600 shadow-md hover:bg-gray-200 hover:scale-105 transition-all" aria-label="Go Back">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>
    
    <header class="max-w-6xl mx-auto px-4 pt-6">
      <div class="bg-gradient-to-r from-teal-500 to-emerald-500 text-white rounded-2xl p-5 shadow-xl flex flex-col md:flex-row items-center gap-4 md:gap-6">
        <div class="flex items-center gap-4">
          <div class="w-20 h-20 rounded-full bg-white/25 flex items-center justify-center text-4xl shadow-md">
            🩺
          </div>
          <div>
            <h1 class="text-2xl md:text-3xl font-extrabold leading-tight">Your Health Dashboard</h1>
            <p class="mt-1 text-sm md:text-base opacity-95">Track your vitals, diet, and overall well-being.</p>
          </div>
        </div>
        <div class="ml-auto flex gap-3">
          <button @click="showProfile = true" class="w-10 h-10 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center">
            ☰
          </button>
        </div>
      </div>
    </header>

    <main class="flex-1 overflow-y-auto p-4 space-y-6 max-w-6xl mx-auto">
      
      <div v-if="nutritionAlert" class="bg-orange-100 border border-orange-200 border-l-4 border-l-orange-500 rounded-xl p-4 shadow-sm">
        <div class="font-semibold text-orange-700 mb-1 flex items-center gap-2 text-base">
          <span class="text-xl">⚠️</span> Nutrition Alert
        </div>
        <div class="text-sm text-orange-900">{{ nutritionAlert }}</div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="bg-white rounded-xl p-5 flex flex-col items-center shadow-md">
          <div class="text-2xl font-bold text-emerald-500">{{ totalCaloriesDisplay }}</div>
          <div class="text-xs text-gray-500">Calories Today</div>
        </div>
        <div class="bg-white rounded-xl p-5 flex flex-col items-center shadow-md">
          <div class="text-2xl font-bold text-emerald-500">{{ waterCount }}/8</div>
          <div class="text-xs text-gray-500">Water Glasses</div>
          <div class="w-full h-2 bg-gray-200 rounded-full mt-2">
            <div class="h-2 bg-emerald-500 rounded-full transition-all duration-300" :style="`width: ${(waterCount / 8) * 100}%`"></div>
          </div>
        </div>
        
        <div v-if="health" class="bg-white rounded-xl p-5 flex flex-col items-center shadow-md lg:col-span-2">
          <div class="text-lg font-bold text-gray-800">Health Status: {{ bmiCategory }}</div>
          <div class="text-sm text-gray-500 mt-1">
            BMI: <span class="font-semibold text-emerald-600">{{ (health.bmi ?? 0).toFixed(1) }}</span> •
            Weight: <span class="font-semibold">{{ health.weight }}kg</span> •
            Height: <span class="font-semibold">{{ health.height }}cm</span>
          </div>
          <div class="text-xs text-gray-400 mt-2">Last updated: {{ lastUpdatedText }}</div>
        </div>
      </div>
      
      <section class="bg-white rounded-2xl p-6 shadow-md">
        <h2 class="text-xl font-bold text-gray-800 mb-4">Quick Actions</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <DietQuickActionCard icon="🍎" title="Log Food" subtitle="Add your meals" @click="goToFoodLog" />
          <DietQuickActionCard icon="💧" title="Track Water" subtitle="Add a glass" @click="goToWater" />
          <DietQuickActionCard icon="⚖️" title="Log Metrics" subtitle="Weight & Vitals" @click="goToHealthMetrics" />
          <DietQuickActionCard icon="💡" title="AI Suggestions" subtitle="Get diet tips" @click="$router.push('/student/nutrition-suggestions')" />
        </div>
      </section>

      <section id="water-section">
        <WaterTracker :model-value="waterCount" @add="onWaterQuickAdd" />
      </section>

      <DietNavigationGrid />
      
    </main>

    <AppModal :show="showLogFood" title="Log Food" size="md" @close="showLogFood = false">
      <LogFoodForm :model-value="foodForm" @submit="submitFood; showLogFood = false" />
    </AppModal>
    <AppModal :show="showLogWeight" title="Log Weight" size="sm" @close="showLogWeight = false">
      <LogWeightForm @submit="submitWeight; showLogWeight = false" />
    </AppModal>
    <ProfileSidebar v-if="showProfile" @close="showProfile = false" />
  </div>
</template>

<script setup>
import StudentNavBar from '@/components/layout/StudentNavBar.vue'
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getWaterSummary, addWater } from '@/services/waterService'
import { getLatestSuggestions } from '@/services/nutritionService'
import { getMeals } from '@/services/dietService'
import { getLatestMetrics } from '@/services/healthService'
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
const waterCount = ref(0)
const showLogFood = ref(false)
const showLogWeight = ref(false)
const totalCalories = ref(0)
const nutritionAlert = ref('')
const totalCaloriesDisplay = computed(() => (totalCalories.value || 0).toLocaleString())

// Health status state
const health = ref(null)
const bmiCategory = computed(() => {
  const bmi = Number(health.value?.bmi ?? 0)
  if (!bmi) return 'Unknown'
  if (bmi < 18.5) return 'Underweight'
  if (bmi < 25) return 'Normal'
  if (bmi < 30) return 'Overweight'
  return 'Obese'
})
const lastUpdatedText = computed(() => {
  const t = health.value?.time
  if (!t) return 'Unknown'
  try {
    const d = new Date(t)
    const today = new Date()
    const isToday = d.toDateString() === today.toDateString()
    if (isToday) return 'Today'
    const diffMs = today.getTime() - d.getTime()
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
    if (diffDays === 1) return 'Yesterday'
    return d.toLocaleString()
  } catch {
    return String(t)
  }
})

const router = useRouter()

async function addWaterHandler() {
  const summary = await addWater(250, 'glass')
  waterCount.value = Math.min(8, Math.round((summary.total_ml || 0) / 250))
}

async function loadNutritionAlert() {
  try {
    const latest = await getLatestSuggestions('today')
    const arr = latest?.suggestions?.alerts || []
    nutritionAlert.value = Array.isArray(arr) && arr.length > 0 ? arr[0] : ''
  } catch (e) {
    nutritionAlert.value = ''
  }
}

onMounted(async () => {
  const summary = await getWaterSummary()
  waterCount.value = Math.min(8, Math.round((summary.total_ml || 0) / 250))
  await loadCalories()
  await loadNutritionAlert()
  await loadHealth()
})

async function onWaterQuickAdd(ml) {
  const summary = await addWater(ml, ml >= 500 ? 'bottle' : ml >= 250 ? 'glass' : 'cup')
  waterCount.value = Math.min(8, Math.round((summary.total_ml || 0) / 250))
}

async function loadCalories() {
  try {
    const rows = await getMeals()
    let sum = 0
    for (const r of rows || []) {
      sum += Math.round(r.calories || 0)
    }
    totalCalories.value = sum
  } catch (e) {
    console.error('Failed to load meals for calories', e)
  }
}

async function loadHealth() {
  try {
    const res = await getLatestMetrics()
    health.value = res
  } catch (e) {
    health.value = null
  }
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
  foodForm.value = { mealType: 'Breakfast', foodName: '', quantity: 1, unit: 'Cup', time: '12:30', notes: '' }
}
function submitWeight(weight) {
  console.log('Weight submitted:', weight)
}
function goToWater() {
  router.push('/student/water')
}
function goToHealthMetrics() {
  router.push('/student/health-metrics')
}
function goToFoodLog() {
  router.push('/student/food-log')
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