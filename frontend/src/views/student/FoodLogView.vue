<template>
    <div class="min-h-screen bg-gray-50 flex flex-col items-center py-6 px-2 md:px-0">
            <button
      @click="$router.go(-1)"
      class="absolute top-4 left-4 z-10 w-10 h-10 flex items-center justify-center rounded-full bg-white text-rose-600 shadow-md hover:bg-rose-100 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-rose-400 transition-all"
      aria-label="Go Back"
    >
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-5 h-5">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>
<div class="w-full max-w-2xl space-y-5">
  <!-- Header -->
  <div class="flex items-center justify-between bg-white rounded-2xl shadow p-3">
    <!-- Back Button -->


    <!-- Title -->
    <h2 class="text-xl font-extrabold text-gray-800 flex items-center gap-2">
      🍎 Today's Meals
    </h2>

    <!-- Add Button -->
    <button
      @click="showLogFood = true"
      class="flex items-center gap-1 px-5 py-2 text-sm rounded-full bg-emerald-500 text-white font-semibold shadow hover:bg-emerald-600 transition-transform hover:scale-105"
    >
      ➕ Add Meal
    </button>
  </div>

  <!-- Food Log List -->
  <FoodLog :meals="meals" />
</div>

        <div class="text-xs text-gray-400 mt-4">Daily Food Log</div>

        <!-- Log Food Modal -->
        <AppModal :isOpen="showLogFood" title="Log Food" size="md" @close="showLogFood = false">
            <LogFoodForm :model-value="foodForm" @submit="onSubmitFood" />
        </AppModal>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import FoodLog from '@/components/diet/FoodLog.vue'
import AppModal from '@/components/ui/AppModal.vue'
import LogFoodForm from '@/components/diet/LogFoodForm.vue'
import { getMeals, logMeal } from '@/services/dietService'

const showLogFood = ref(false)
const meals = ref([])

const foodForm = ref({
    mealType: 'Breakfast',
    foodName: '',
    quantity: 1,
    unit: 'Cup',
    time: '12:30',
    notes: ''
})

const MEAL_META = {
    breakfast: { label: '🌅 Breakfast', icon: '🌅' },
    lunch: { label: '🌞 Lunch', icon: '🌞' },
    dinner: { label: '🍽️ Dinner', icon: '🍽️' },
    snacks: { label: '🧃 Snacks', icon: '🧃' },
}

function toMealTypeKey(label) {
    // UI label -> DB key
    if (!label) return 'snacks'
    const map = { Breakfast: 'breakfast', Lunch: 'lunch', Dinner: 'dinner', Snack: 'snacks', Snacks: 'snacks' }
    return map[label] || 'snacks'
}

function formatTime(iso) {
    if (!iso) return ''
    try {
        const d = new Date(iso)
        return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    } catch {
        return ''
    }
}

function transformMeals(rows) {
    const grouped = {
        breakfast: { type: MEAL_META.breakfast.label, icon: MEAL_META.breakfast.icon, totalCalories: 0, items: [] },
        lunch: { type: MEAL_META.lunch.label, icon: MEAL_META.lunch.icon, totalCalories: 0, items: [] },
        dinner: { type: MEAL_META.dinner.label, icon: MEAL_META.dinner.icon, totalCalories: 0, items: [] },
        snacks: { type: MEAL_META.snacks.label, icon: MEAL_META.snacks.icon, totalCalories: 0, items: [] },
    }
    for (const r of rows || []) {
        const key = (r.mealtype || 'snacks').toLowerCase()
        const bucket = grouped[key] || grouped.snacks
        bucket.totalCalories += Math.round(r.calories || 0)
        bucket.items.push({
            icon: '🍽️',
            name: r.description || 'Food Item',
            quantity: '',
            time: formatTime(r.time),
            calories: Math.round(r.calories || 0),
            proteins: Number(r.proteins || 0),
            carbs: Number(r.carbs || 0),
            fat: Number(r.fat || 0),
        })
    }
    // Only show groups that have items to avoid empty 'snacks' blocks
    return Object.values(grouped).filter(g => g.items.length > 0)
}

async function loadMeals() {
    const rows = await getMeals()
    meals.value = transformMeals(rows)
}

onMounted(loadMeals)

async function onSubmitFood(form) {
    // Build description including quantity and unit
    const description = form.foodName?.trim() || ''
    if (!description) {
        // Silently ignore accidental empty submissions
        return
    }
    const fullDescription = `${form.quantity || 1} ${form.unit || ''} ${description}`.trim()
    const mealtype = toMealTypeKey(form.mealType)

    await logMeal({
        mealtype,
        description: fullDescription,
    })
    showLogFood.value = false
    // Reset form for next open
    foodForm.value = { mealType: 'Breakfast', foodName: '', quantity: 1, unit: 'Cup', time: '12:30', notes: '' }
    await loadMeals()
}
</script>