<template>
  <div class="min-h-screen bg-gray-50">
    <StudentNavBar />
    <div class="bg-gray-100 font-sans p-4 md:p-6">
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-gray-800">Finance Management</h1>
        <AppButton label="Add Transaction" variant="primary" @click="addTransaction" />
      </div>

      <div class="flex flex-wrap gap-2 items-center">
        <!-- Custom date range -->
        <div class="flex items-center gap-2">
          <input type="date" v-model="customFrom" class="border rounded px-2 py-1" />
          <span>-</span>
          <input type="date" v-model="customTo" class="border rounded px-2 py-1" />
          <button @click="applyCustomRange" class="bg-green-500 text-white px-3 py-1 rounded">
            Apply
          </button>
        </div>
      </div>

      <br>

      <!-- Key Metrics -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-xl shadow p-6 text-center">
          <span class="text-3xl mb-2">💰</span>
          <div class="font-bold text-lg text-gray-800">₹{{ dashboard.balance }}</div>
          <div class="text-sm text-gray-500">Total Balance</div>
        </div>
        <div class="bg-white rounded-xl shadow p-6 text-center">
          <span class="text-3xl mb-2">📈</span>
          <div class="font-bold text-lg text-green-600">₹{{ dashboard.month_income }}</div>
          <div class="text-sm text-gray-500">Income</div>
        </div>
        <div class="bg-white rounded-xl shadow p-6 text-center">
          <span class="text-3xl mb-2">📉</span>
          <div class="font-bold text-lg text-red-600">₹{{ dashboard.month_expenses }}</div>
          <div class="text-sm text-gray-500">Expenses</div>
        </div>
        <div class="bg-white rounded-xl shadow p-6 text-center">
          <span class="text-3xl mb-2">🎯</span>
          <div class="font-bold text-lg text-blue-600">$500</div>
          <div class="text-sm text-gray-500">Savings Goal</div>
        </div>
      </div>

      <!-- Savings Goals Section -->
      <div class="mt-8">
        <h2 class="text-xl font-bold text-gray-800 mb-4">Savings Goals</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <AppCard v-for="goal in savingsGoals" :key="goal.id">
            <div class="flex justify-between items-start mb-3">
              <h3 class="font-semibold text-gray-800">{{ goal.title }}</h3>
              <span class="text-sm text-gray-500">₹{{ goal.saved }}/₹{{ goal.target }}</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2 mb-3">
              <div
                class="bg-blue-600 h-2 rounded-full"
                :style="{ width: `${Math.min((goal.saved / goal.target) * 100, 100)}%` }"
              ></div>
            </div>
            <div class="flex justify-between text-sm text-gray-600">
              <span>{{ Math.round((goal.saved / goal.target) * 100) }}% Complete</span>
              <span>₹{{ goal.target - goal.saved }} to go</span>
            </div>
          </AppCard>
        </div>
      </div>

      <!-- Filters and Category -->
      <div>
        <div class="flex space-x-2 mb-6 border-b border-gray-200 pb-3">
          <button
            v-for="filter in filters"
            :key="filter"
            @click="activeFilter = filter"
            :class="[
              'px-4 py-2 text-sm font-semibold rounded-full',
              activeFilter === filter ? 'bg-blue-600 text-white' : 'bg-white text-gray-700'
            ]"
          >
            {{ filter }}
          </button>
        </div>
        <label for="categorySelect" class="block mb-1 font-semibold">Select Category</label>
        <select
          id="categorySelect"
          v-model="selectedCategory"
          class="border rounded px-3 py-1 mb-6 w-full max-w-xs"
        >
          <option value="">All Categories</option>
          <option
            v-for="cat in categories"
            :key="cat"
            :value="cat"
          >
            {{ cat }}
          </option>
        </select>
      </div>

      <!-- Transaction List -->
      <div class="space-y-4">
        <AppCard
          v-for="transaction in filteredTransactions"
          :key="transaction.transaction_id"
          :class="transactionBorder(transaction.type)"
        >
          <div class="flex flex-col md:flex-row md:justify-between">
            <!-- Transaction Info -->
            <div class="flex-grow mb-4 md:mb-0">
              <div class="flex items-center mb-2">
                <span
                  :class="[
                    'text-sm font-bold',
                    transaction.type === 'Income' ? 'text-green-400' : 'text-red-400',
                    transactionBackground(transaction.type)
                  ]"
                >
                  {{ transaction.type }}
                </span>
                <h3 class="text-lg font-bold text-gray-800 ml-2">{{ transaction.note }}</h3>
              </div>
              <div class="flex items-center text-sm text-gray-500 mb-2">
                <span class="mr-4"><strong>Category:</strong> {{ transaction.category }}</span>
                <span><strong>Date:</strong> {{ transaction.transaction_date }}</span>
              </div>
            </div>

            <!-- Amount and Actions -->
            <div class="flex flex-col md:items-end md:justify-between space-y-2">
              <div class="text-right">
                <div
                  :class="[
                    'text-lg font-bold',
                    transaction.type === 'Income' ? 'text-green-600' : 'text-red-600'
                  ]"
                >
                  {{ transaction.type === 'Income' ? '+' : '-' }}₹{{ transaction.amount }}
                </div>
              </div>
              <div class="flex space-x-2 justify-end">
                <AppButton label="Edit" variant="secondary" size="sm" />
                <AppButton 
                  label="Delete" 
                  variant="error" 
                  size="sm" 
                  @click="requestDelete(transaction)" 
                />
              </div>
            </div>
          </div>
        </AppCard>

        <div v-if="filteredTransactions.length === 0" class="text-center py-8">
          <div class="text-gray-400 mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-700">No Transactions Yet</h3>
          <p class="text-gray-500 mt-1">Start tracking your finances by adding your first transaction</p>
          <AppButton label="Add Transaction" variant="primary" class="mt-4" @click="addTransaction" />
        </div>
      </div>

      <!-- Delete Confirmation Modal -->
      <div 
        v-if="showDeleteConfirm" 
        class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
      >
        <div class="bg-white rounded-lg p-6 max-w-sm w-full shadow-lg">
          <h3 class="text-lg font-semibold mb-4">Confirm Delete</h3>
          <p class="mb-6">Are you sure you want to delete this transaction?</p>
          <div class="flex justify-end space-x-4">
            <button 
              @click="cancelDelete" 
              class="px-4 py-2 rounded border border-gray-300 hover:bg-gray-100"
            >
              Cancel
            </button>
            <button 
              @click="confirmDelete" 
              class="px-4 py-2 rounded bg-red-600 text-white hover:bg-red-700"
            >
              Delete
            </button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import StudentNavBar from '@/components/layout/StudentNavBar.vue'
import AppCard from '@/components/ui/AppCard.vue'
import AppButton from '@/components/ui/AppButton.vue'
import { fetchDashboardData } from '@/services/finservice'

export default {
  name: 'StudentFinanceView',
  components: {
    StudentNavBar,
    AppCard,
    AppButton,
  },
  setup() {
    
    const router = useRouter()

    // Reactive state
    const dashboard = ref({})
    const filters = ['All', 'Income', 'Expense']
    const activeFilter = ref('All')
    const selectedCategory = ref('')
    const customFrom = ref('')
    const customTo = ref('')
    const transactionToDelete = ref(null)  // Store selected transaction for delete confirmation
    const showDeleteConfirm = ref(false) 
    const transactions = ref([])
    const savingsGoals = ref([
      { id: 1, title: 'New Gaming Console', target: 500, saved: 320 },
      { id: 2, title: 'College Fund', target: 2000, saved: 450 },
    ])

    const categories = computed(() => {
      // Unique categories from transactions
      const cats = new Set()
      transactions.value.forEach(t => {
        if (t.category) cats.add(t.category)
      })
      return [...cats]
    })

    // Filter transactions based on activeFilter and selectedCategory
    const filteredTransactions = computed(() => {
      let result = transactions.value

      if (activeFilter.value !== 'All') {
        result = result.filter(t =>
          t.type.toLowerCase() === activeFilter.value.toLowerCase()
        )
      }

      if (selectedCategory.value) {
        result = result.filter(t => t.category === selectedCategory.value)
      }

      return result
    })

    // UI class helpers
    const transactionClasses = {
      'Income': { border: 'border-l-4 border-green-500', bg: 'bg-green-100 text-green-800' },
      'Expense': { border: 'border-l-4 border-red-500', bg: 'bg-red-100 text-red-800' },
    }

    function transactionBorder(type) {
      return transactionClasses[type]?.border || 'border-l-4 border-gray-300'
    }

    function transactionBackground(type) {
      return transactionClasses[type]?.bg || 'bg-gray-100 text-gray-800'
    }

    // Delete confirmation modal control
    function requestDelete(transaction) {
      transactionToDelete.value = transaction
      showDeleteConfirm.value = true
    }

    function cancelDelete() {
      transactionToDelete.value = null
      showDeleteConfirm.value = false
    }

    function confirmDelete() {
      if (transactionToDelete.value) {
        // Remove from transactions list (local delete)
        transactions.value = transactions.value.filter(t => t.transaction_id !== transactionToDelete.value.transaction_id)

        // TODO: Call backend API to delete permanently if you have one

        // Clear and close modal
        transactionToDelete.value = null
        showDeleteConfirm.value = false
      }
    }

    // Fetch dashboard data on mount or when applying filters
    async function loadDashboard(range = 'last30', fromDate = '', toDate = '') {
      let params = {}
      if (range === 'custom' && fromDate && toDate) {
        params = { from_date: fromDate, to_date: toDate }
      } else {
        params = { range }
      }
      const data = await fetchDashboardData(params)
      dashboard.value = data
      transactions.value = data.transactions || []
    }

    // Called on filter click - fetch data again if needed
    async function selectRange(value) {
      await loadDashboard(value)
    }

    // Apply custom date range filter
    async function applyCustomRange() {
      if (!customFrom.value || !customTo.value) return
      await loadDashboard('custom', customFrom.value, customTo.value)
    }

    function addTransaction() {
      router.push('/student/addtransaction')
    }

    // On component mounted
    onMounted(async () => {
      await loadDashboard()
    })

    return {
      dashboard,
      filters,
      activeFilter,
      selectedCategory,
      customFrom,
      customTo,
      transactions,
      savingsGoals,
      categories,
      filteredTransactions,
      transactionBorder,
      transactionBackground,
      selectRange,
      applyCustomRange,
      addTransaction,
      requestDelete,
      cancelDelete,
      confirmDelete,
      showDeleteConfirm,
    }
  },
}
</script>
