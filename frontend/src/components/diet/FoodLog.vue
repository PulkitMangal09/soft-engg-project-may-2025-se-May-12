<template>
  <div class="bg-white rounded-3xl shadow p-6 space-y-6">
    
    <!-- Header
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-bold flex items-center gap-2">
      </h2>
      <slot name="add"></slot>
    </div> -->

    <!-- Summary Stats -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <div v-for="stat in stats" :key="stat.label"
        class="bg-pink-50 rounded-2xl p-4 text-center shadow-sm">
        <div class="text-2xl">{{ stat.icon }}</div>
        <div class="text-lg font-bold text-pink-600">{{ stat.value }}</div>
        <div class="text-xs text-gray-500">{{ stat.label }}</div>
      </div>
    </div>

    <!-- Meals -->
    <div v-for="meal in meals" :key="meal.type" class="space-y-3">
      
      <!-- Meal Header -->
      <div class="flex items-center justify-between bg-pink-100 rounded-xl px-4 py-2">
        <div class="font-semibold text-pink-700 flex items-center gap-2">
          {{ meal.icon }} {{ meal.type }}
        </div>
        <div class="text-pink-700 font-semibold text-sm">
          {{ meal.totalCalories }} cal
        </div>
      </div>

      <!-- Meal Items -->
      <div v-for="item in meal.items" :key="item.name"
        class="flex items-center bg-white rounded-xl p-3 shadow-sm border border-gray-100">
        <div class="w-12 h-12 rounded-xl bg-pink-50 flex items-center justify-center text-2xl mr-3">
          {{ item.icon }}
        </div>
        <div class="flex-1">
          <div class="font-semibold text-gray-800">{{ item.name }}</div>
          <div class="text-xs text-gray-400">
            {{ item.quantity }} • {{ item.time }}
          </div>
        </div>
        <div class="font-semibold text-pink-600">
          {{ item.calories }} cal
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  meals: {
    type: Array,
    required: true
  }
})

const flatItems = computed(() => (props.meals || []).flatMap(m => m.items || []))

const totals = computed(() => {
  const sum = { calories: 0, proteins: 0, carbs: 0, fat: 0 }
  for (const it of flatItems.value) {
    sum.calories += Number(it.calories || 0)
    sum.proteins += Number(it.proteins || 0)
    sum.carbs += Number(it.carbs || 0)
    sum.fat += Number(it.fat || 0)
  }
  return {
    calories: Math.round(sum.calories),
    proteins: Math.round(sum.proteins),
    carbs: Math.round(sum.carbs),
    fat: Math.round(sum.fat),
  }
})

const stats = computed(() => [
  { label: 'Calories', value: totals.value.calories, icon: '🔥' },
  { label: 'Carbs', value: `${totals.value.carbs}g`, icon: '🍞' },
  { label: 'Protein', value: `${totals.value.proteins}g`, icon: '🍗' },
  { label: 'Fat', value: `${totals.value.fat}g`, icon: '🥑' }
])
</script>
