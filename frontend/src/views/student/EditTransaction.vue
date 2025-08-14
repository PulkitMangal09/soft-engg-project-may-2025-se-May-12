<template>
  <div class="max-w-xl mx-auto p-6 bg-white shadow-lg rounded-xl mt-6">
    <h2 class="text-2xl font-bold mb-6 text-blue-600">Edit Transaction</h2>

    <form class="space-y-4" @submit.prevent="handleSubmit">
      <!-- Amount -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Amount</label>
        <input
          v-model="form.amount"
          type="number"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
          required
        />
      </div>

      <!-- Type -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Type</label>
        <select
          v-model="form.type"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500">
          <option>Income</option>
          <option>Expense</option>
        </select>
      </div>

      <!-- Category -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Category</label>
        <input
          v-model="form.category"
          type="text"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
          required
        />
      </div>

      <!-- Note -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Note</label>
        <input
          v-model="form.note"
          type="text"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
        />
      </div>

      <!-- Date -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Date</label>
        <input
          v-model="form.date"
          type="date"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
        />
      </div>

      <!-- Submit Button -->
      <div class="pt-4">
     <button
  type="submit"
  class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-md"
>
  Update Transaction
</button>

      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getTransaction, updateTransaction} from '@/services/finservice'

const route = useRoute()
const router = useRouter()

const form = ref({
  amount: '',
  type: 'Income',
  category: '',
  note: '',
  date: ''
})

const transaction = ref(null)

onMounted(async () => {
  const id = route.params.id
  if (id) {
    try {
      transaction.value = await getTransaction(id)
      form.value = {
        amount: transaction.value.amount,
        type: transaction.value.type,
        category: transaction.value.category,
        note: transaction.value.note,
        date: transaction.value.transaction_date
      }
    } catch (err) {
      console.error('Error fetching transaction:', err)
    }
  }
})

const handleSubmit = async () => {
  if (!transaction.value) return;
  try {
    await updateTransaction(transaction.value.transaction_id, form.value);
    router.push('/student/finance'); // redirect back after update
  } catch (err) {
    console.error('Error updating transaction:', err);
  }
}


</script>
