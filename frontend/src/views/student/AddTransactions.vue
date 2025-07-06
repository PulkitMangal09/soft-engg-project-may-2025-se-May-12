<template>
  <div class="max-w-xl mx-auto p-6 bg-white shadow-lg rounded-xl mt-6">
    <h2 class="text-2xl font-bold mb-6 text-blue-600">Add Transaction</h2>

    <form class="space-y-4">
      <!-- Amount -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Amount</label>
        <input
          type="number"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
          placeholder="₹"
        />
      </div>

      <!-- Type -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Type</label>
        <select
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
        >
          <option>Income</option>
          <option>Expense</option>
        </select>
      </div>

      <!-- Category -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Category</label>
        <input
          type="text"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
          placeholder="e.g., Snacks, Pocket Money"
        />
      </div>

      <!-- Note -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Note</label>
        <input
          type="text"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
          placeholder="optional note..."
        />
      </div>

<!-- Date -->
<div>
  <label class="block text-sm font-medium text-gray-700">Date</label>
  <input
    type="date"
    v-model="form.date"
    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
  />
</div>


      <!-- Submit Button -->
      <div class="pt-4">
        <button
          type="submit"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-md"
        >
          Add Transaction
        </button>
      </div>
    </form>
  </div>
</template>


<script setup>
import { ref } from 'vue'

// Utility: format today as YYYY-MM-DD
const today = new Date().toISOString().split('T')[0]

// Form state
const form = ref({
  amount: '',
  type: 'Income',
  category: '',
  note: '',
  date: today // Set default to today
})
</script>


<script>
export default {
    name: 'AddTransactions'
}
</script>