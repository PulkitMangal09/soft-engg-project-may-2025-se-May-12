<template>
  <div class="bg-white rounded-3xl shadow p-6 space-y-6">
    <!-- Header -->
    <h2 class="text-xl font-bold flex items-center gap-2">
      🍽️ Log a Meal
    </h2>

    <form class="space-y-5" @submit.prevent="$emit('submit', form)">

      <!-- Meal Type -->
      <div>
        <label class="block text-sm font-semibold mb-2">Meal Type</label>
        <div class="grid grid-cols-4 gap-2">
          <button
            v-for="type in mealTypes"
            :key="type.label"
            type="button"
            @click="form.mealType = type.label"
            :class="[
              'rounded-xl p-3 flex flex-col items-center border-2 transition',
              form.mealType === type.label
                ? 'bg-pink-100 border-pink-400'
                : 'bg-gray-50 border-gray-200 hover:border-pink-300'
            ]"
          >
            <span class="text-lg">{{ type.icon }}</span>
            <span class="text-xs mt-1 font-medium">{{ type.label }}</span>
          </button>
        </div>
      </div>

      <!-- Food Name -->
      <div>
        <label class="block text-sm font-semibold mb-2">Food Item</label>
        <input
          v-model="form.foodName"
          type="text"
          placeholder="Search or type food name"
          class="w-full border-2 border-gray-200 rounded-xl px-4 py-2 focus:border-pink-400 focus:outline-none"
        />
      </div>

      <!-- Quantity & Unit -->
      <div>
        <label class="block text-sm font-semibold mb-2">Quantity</label>
        <div class="flex gap-2">
          <input
            v-model.number="form.quantity"
            type="number"
            min="1"
            class="w-1/3 border-2 border-gray-200 rounded-xl px-3 py-2 focus:border-pink-400 focus:outline-none"
          />
          <select
            v-model="form.unit"
            class="w-2/3 border-2 border-gray-200 rounded-xl px-3 py-2 focus:border-pink-400 focus:outline-none"
          >
            <option>Cup</option>
            <option>Piece</option>
            <option>Tablespoon</option>
            <option>Grams</option>
            <option>Bowl</option>
          </select>
        </div>
      </div>

      <!-- Time -->
      <div>
        <label class="block text-sm font-semibold mb-2">Time</label>
        <input
          v-model="form.time"
          type="time"
          class="w-full border-2 border-gray-200 rounded-xl px-4 py-2 focus:border-pink-400 focus:outline-none"
        />
      </div>

      <!-- Submit -->
      <div class="pt-3 flex justify-center">
        <button
          type="submit"
          class="bg-pink-400 text-white font-semibold rounded-full px-6 py-2 hover:bg-pink-500 shadow"
        >
          Log Food
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  modelValue: Object
})

const mealTypes = [
  { label: 'Breakfast', icon: '🌅' },
  { label: 'Lunch', icon: '🌞' },
  { label: 'Dinner', icon: '🌙' },
  { label: 'Snack', icon: '🍪' }
]

const form = reactive({
  mealType: 'Breakfast',
  foodName: '',
  quantity: 1,
  unit: 'Cup',
  time: '12:30',
  notes: ''
})

watch(() => props.modelValue, (val) => {
  if (val) Object.assign(form, val)
}, { immediate: true })
</script>
