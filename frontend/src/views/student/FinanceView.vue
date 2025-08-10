<template>
  <div class="min-h-screen bg-gray-50">
    <StudentNavBar />
    <div class="bg-gray-100 font-sans p-4 md:p-6">
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-gray-800">Finance Management</h1>
        <AppButton label="+ Add Transaction" variant="primary" @click="addTransaction" />
      </div>

      <!-- Key Metrics -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-xl shadow p-6 text-center">
          <span class="text-3xl mb-2">💰</span>
          <div class="font-bold text-lg text-gray-800">$1,250</div>
          <div class="text-sm text-gray-500">Total Balance</div>
        </div>
        <div class="bg-white rounded-xl shadow p-6 text-center">
          <span class="text-3xl mb-2">📈</span>
          <div class="font-bold text-lg text-green-600">$450</div>
          <div class="text-sm text-gray-500">Income This Month</div>
        </div>
        <div class="bg-white rounded-xl shadow p-6 text-center">
          <span class="text-3xl mb-2">📉</span>
          <div class="font-bold text-lg text-red-600">$320</div>
          <div class="text-sm text-gray-500">Expenses This Month</div>
        </div>
        <div class="bg-white rounded-xl shadow p-6 text-center">
          <span class="text-3xl mb-2">🎯</span>
          <div class="font-bold text-lg text-blue-600">$500</div>
          <div class="text-sm text-gray-500">Savings Goal</div>
        </div>
      </div>

      <!-- Filters -->
      <div class="flex space-x-2 mb-6 border-b border-gray-200 pb-3">
        <button 
          v-for="filter in filters" 
          :key="filter"
          @click="activeFilter = filter"
          :class="['px-4 py-2 text-sm font-semibold rounded-full', activeFilter === filter ? 'bg-blue-600 text-white' : 'bg-white text-gray-700']"
        >
          {{ filter }} ({{ filteredTransactions.length }})
        </button>
      </div>

      <!-- Transaction List -->
      <div class="space-y-4">
        <AppCard v-for="transaction in filteredTransactions" :key="transaction.id" :class="transactionBorder(transaction.type)">
          <div class="flex flex-col md:flex-row md:justify-between">
            <!-- Transaction Info -->
            <div class="flex-grow mb-4 md:mb-0">
              <div class="flex items-center mb-2">
                <span :class="['px-2 py-0.5 text-xs font-semibold rounded-full mr-3', transactionBackground(transaction.type)]">
                  {{ transaction.type }}
                </span>
                <h3 class="text-lg font-bold text-gray-800">{{ transaction.title }}</h3>
              </div>
              <div class="flex items-center text-sm text-gray-500 mb-2">
                <span class="mr-4"><strong>Category:</strong> {{ transaction.category }}</span>
                <span><strong>Date:</strong> {{ transaction.date }}</span>
              </div>
              <p class="text-sm text-gray-600" v-if="transaction.note">{{ transaction.note }}</p>
            </div>
            <!-- Amount and Actions -->
            <div class="flex flex-col md:items-end md:justify-between space-y-2">
              <div class="text-right">
                <div :class="['text-lg font-bold', transaction.type === 'credit' ? 'text-green-600' : 'text-red-600']">
                  {{ transaction.type === 'credit' ? '+' : '-' }}${{ transaction.amount }}
                </div>
              </div>
              <div class="flex space-x-2 justify-end">
                <AppButton label="Edit" variant="secondary" size="sm" />
                <AppButton label="Delete" variant="error" size="sm" />
              </div>
            </div>
          </div>
        </AppCard>
        
        <div v-if="filteredTransactions.length === 0" class="text-center py-8">
          <div class="text-gray-400 mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-700">No Transactions Yet</h3>
          <p class="text-gray-500 mt-1">Start tracking your finances by adding your first transaction</p>
          <AppButton label="Add Transaction" variant="primary" class="mt-4" @click="addTransaction" />
        </div>
      </div>

      <!-- Savings Goals Section -->
      <div class="mt-8">
        <h2 class="text-xl font-bold text-gray-800 mb-4">Savings Goals</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <AppCard v-for="goal in savingsGoals" :key="goal.id">
            <div class="flex justify-between items-start mb-3">
              <h3 class="font-semibold text-gray-800">{{ goal.title }}</h3>
              <span class="text-sm text-gray-500">${{ goal.saved }}/${{ goal.target }}</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2 mb-3">
              <div 
                class="bg-blue-600 h-2 rounded-full" 
                :style="{ width: `${Math.min((goal.saved / goal.target) * 100, 100)}%` }"
              ></div>
            </div>
            <div class="flex justify-between text-sm text-gray-600">
              <span>{{ Math.round((goal.saved / goal.target) * 100) }}% Complete</span>
              <span>${{ goal.target - goal.saved }} to go</span>
            </div>
          </AppCard>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import StudentNavBar from '@/components/layout/StudentNavBar.vue'
import AppCard from '@/components/ui/AppCard.vue'
import AppButton from '@/components/ui/AppButton.vue'

export default {
  name: 'StudentFinanceView',
  components: {
    StudentNavBar,
    AppCard,
    AppButton,
  },
  setup() {
    const filters = ['All', 'Credit', 'Debit']
    const activeFilter = ref('All')

    const transactions = ref([
      { 
        id: 1, 
        title: 'Allowance from Parents', 
        type: 'credit', 
        category: 'Allowance',
        amount: 100,
        date: '2025-01-15',
        note: 'Weekly allowance'
      },
      { 
        id: 2, 
        title: 'Lunch at School', 
        type: 'debit', 
        category: 'Food',
        amount: 8.50,
        date: '2025-01-15',
        note: 'School cafeteria'
      },
      { 
        id: 3, 
        title: 'Birthday Gift Money', 
        type: 'credit', 
        category: 'Gift',
        amount: 50,
        date: '2025-01-14',
        note: 'From Grandma'
      },
      { 
        id: 4, 
        title: 'Movie Tickets', 
        type: 'debit', 
        category: 'Entertainment',
        amount: 24,
        date: '2025-01-13',
        note: 'Weekend movie with friends'
      },
    ])

    const savingsGoals = ref([
      {
        id: 1,
        title: 'New Gaming Console',
        target: 500,
        saved: 320
      },
      {
        id: 2,
        title: 'College Fund',
        target: 2000,
        saved: 450
      }
    ])

    const filteredTransactions = computed(() => {
      if (activeFilter.value === 'All') return transactions.value
      return transactions.value.filter(transaction => 
        transaction.type === activeFilter.value.toLowerCase()
      )
    })

    const transactionClasses = {
      'credit': { border: 'border-l-4 border-green-500', bg: 'bg-green-100 text-green-800' },
      'debit': { border: 'border-l-4 border-red-500', bg: 'bg-red-100 text-red-800' },
    }

    function transactionBorder(type) {
      return transactionClasses[type]?.border || 'border-l-4 border-gray-300'
    }

    function transactionBackground(type) {
      return transactionClasses[type]?.bg || 'bg-gray-100 text-gray-800'
    }

    function addTransaction() {
      // In real app, this would open a modal or navigate to add transaction page
      console.log('Add transaction clicked')
    }

    return {
      filters,
      activeFilter,
      transactions,
      savingsGoals,
      filteredTransactions,
      transactionBorder,
      transactionBackground,
      addTransaction
    }
  },
}
</script>
