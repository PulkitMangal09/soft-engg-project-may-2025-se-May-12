<template>
  <div class="max-w-xl mx-auto p-6 bg-white shadow-lg rounded-xl mt-6">
    <h2 class="text-2xl font-bold mb-6 text-blue-600">Add Savings Goal</h2>

    <form class="space-y-4" @submit.prevent="handleSubmit">
      <!-- Title -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Goal Title</label>
        <input
          v-model="form.title"
          type="text"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
          placeholder="e.g., New Laptop, College Fund"
          required
        />
      </div>

      <!-- Target Amount -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Target Amount</label>
        <input
          v-model="form.target_amount"
          type="number"
          step="0.01"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
          placeholder="₹"
          required
        />
      </div>

      <!-- Submit Button -->
  <!-- Submit Button -->
<div class="pt-4">
  <button
    type="submit"
    :disabled="loading"
    class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
  >
    <span v-if="loading">Adding...</span>
    <span v-else>Add Goal</span>
  </button>

  <p v-if="error" class="text-red-600 mt-2 text-sm">{{ error }}</p>
</div>

    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { createSavingsGoal } from '@/services/finservice'

const router = useRouter()

const form = ref({
  title: '',
  target_amount: ''
})

const loading = ref(false)
const error = ref(null)

const handleSubmit = async () => {
  loading.value = true
  error.value = null

  try {
    const payload = {
      title: form.value.title,
      target_amount: parseFloat(form.value.target_amount)
    }
    await createSavingsGoal(payload)
    router.push('/student/finance')
  } catch (err) {
    console.error('Error adding savings goal:', err)
    error.value = 'Could not add goal. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
