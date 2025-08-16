  <template>
    <div class="min-h-screen bg-gray-50">
      <StudentNavBar />
      <div class="bg-gray-100 font-sans p-4 md:p-6">
        <!-- Header -->
      <div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold text-gray-800">Finance Management</h1>
    <div class="flex gap-2">
      <AppButton 
        label="Add Transaction" 
        variant="primary" 
        @click="addTransaction" 
      />
      <AppButton 
        label="Add Goal" 
        variant="secondary" 
        @click="addGoal" 
      />
    </div>
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
    
        </div>

        <!-- Savings Goals Section -->
        <div class="mt-8">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Savings Goals</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <AppCard v-for="goal in savingsGoals" :key="goal.goal_id">
  <div class="flex justify-between items-start mb-3">
    <h3 class="font-semibold text-gray-800">{{ goal.title }}</h3>
    <span class="text-sm text-gray-500">₹{{ goal.saved_amount }}/₹{{ goal.target_amount }}</span>
  </div>

  <div class="w-full bg-gray-200 rounded-full h-2 mb-3">
    <div
      class="bg-blue-600 h-2 rounded-full"
      :style="{ width: `${Math.min((goal.saved_amount / goal.target_amount) * 100, 100)}%` }"
    ></div>
  </div>

  <div class="flex justify-between text-sm text-gray-600 mb-3">
    <span>{{ Math.round((goal.saved_amount / goal.target_amount) * 100) }}% Complete</span>
    <span>₹{{ goal.target_amount - goal.saved_amount }} to go</span>
  </div>

  <!-- Action Buttons -->
<!-- Action buttons -->
        <div class="flex justify-between gap-2">
          <AppButton variant="primary" size="sm" @click="requestContribution(goal)">
            Contribute
          </AppButton>
          <AppButton variant="secondary" size="sm" @click="editGoal(goal)">
            Edit
          </AppButton>
          <AppButton variant="error" size="sm" @click="requestGoalDelete(goal)">
            Delete
          </AppButton>
        </div>
</AppCard>
<div v-if="showContributionModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-xl shadow-lg w-full max-w-sm">
        <h2 class="text-lg font-bold mb-4">Add to {{ selectedGoal?.title }}</h2>

        <input type="number" v-model="contributionAmount"placeholder="Enter amount" class="w-full border border-gray-300 rounded-md p-2 mb-4" required/>

        <div class="flex justify-end gap-2">
          <AppButton variant="secondary" @click="cancelContribution">Cancel</AppButton>
          <AppButton variant="primary" @click="confirmContribution">Confirm</AppButton>
        </div>
      </div>
    </div>
      <!-- Delete Confirmation Modal -->
  <div
    v-if="showGoalDeleteConfirm"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white p-6 rounded-lg w-96 shadow-lg">
      <h3 class="text-lg font-bold mb-4">Confirm Delete</h3>
      <p class="mb-6">
        Are you sure you want to delete the goal
        <strong>{{ goalToDelete }}</strong>?
      </p>
      <div class="flex justify-end space-x-3">
        <button
          @click="cancelGoalDelete"
          class="px-4 py-2 rounded bg-gray-200 text-gray-700 hover:bg-gray-300"
        >
          Cancel
        </button>
        <button
          @click="confirmGoalDelete"
          class="px-4 py-2 rounded bg-red-600 text-white hover:bg-red-700"
        >
          Delete
        </button>
      </div>
    </div>
  </div>

          </div>
        </div>
        <br>
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
                                    <AppButton
                      label="Edit"
                      variant="secondary"
                      size="sm"
                      @click="editTransaction(transaction)"
                    />

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
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white p-6 rounded-lg w-96 shadow-lg">
      <h3 class="text-lg font-bold mb-4">Confirm Delete</h3>
      <p class="mb-6">
        Are you sure you want to delete the transaction
        <strong>{{ transactionToDelete?.note }}</strong>?
      </p>
      <div class="flex justify-end space-x-3">
        <button
          @click="cancelDelete"
          class="px-4 py-2 rounded bg-gray-200 text-gray-700 hover:bg-gray-300"
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
  import { deleteTransaction } from '@/services/finservice'
  import { contributeToGoal } from '@/services/finservice'
  import { deleteGoal } from '@/services/finservice'

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
    const transactionToDelete = ref(null)
    const goalToDelete = ref(null)
    const goalToContribute = ref(null)
    const contributionAmount = ref(0)
    const showDeleteConfirm = ref(false)
    const showGoalDeleteConfirm = ref(false)
    const showContributionModal = ref(false)
    const transactions = ref([])
    const savingsGoals = ref([])
    const showContributeModal = ref(false)
    const selectedGoal = ref(null)



    const categories = computed(() => {
      const cats = new Set()
      transactions.value.forEach(t => {
        if (t.category) cats.add(t.category)
      })
      return [...cats]
    })

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

    // Transaction delete
    function requestDelete(transaction) {
      transactionToDelete.value = transaction
      showDeleteConfirm.value = true
    }
    function cancelDelete() {
      transactionToDelete.value = null
      showDeleteConfirm.value = false
    }
    async function confirmDelete() {
      if (!transactionToDelete.value) return
      try {
        await deleteTransaction(transactionToDelete.value.transaction_id)
        transactions.value = transactions.value.filter(
          t => t.transaction_id !== transactionToDelete.value.transaction_id
        )
        showDeleteConfirm.value = false
        transactionToDelete.value = null
      } catch (err) {
        console.error('Failed to delete transaction:', err)
      }
    }

    // Goal delete
    function requestGoalDelete(goal) {

      goalToDelete.value = goal
      showGoalDeleteConfirm.value = true
    }
    function cancelGoalDelete() {
      goalToDelete.value = null
      showGoalDeleteConfirm.value = false
    }
    async function confirmGoalDelete() {
      if (!goalToDelete.value) return
      try {
        await deleteGoal(goalToDelete.value.goal_id)
        savingsGoals.value = savingsGoals.value.filter(g => g.id !== goalToDelete.value.id)
        showGoalDeleteConfirm.value = false
        goalToDelete.value = null
        await loadDashboard()
      } catch (err) {
        console.error('Failed to delete goal:', err)
      }
    }

    // Contribution flow
    function requestContribution(goal) {
      goalToContribute.value = goal
      contributionAmount.value = ''
      showContributionModal.value = true
    }
    function cancelContribution() {
      goalToContribute.value = null
      showContributionModal.value = false
    }
    async function confirmContribution() {
      //if (!goalToContribute.value || !contributionAmount.value) return
      try {
        await contributeToGoal(goalToContribute.value.goal_id, contributionAmount.value)
        // Refresh or update local goal progress
        await loadDashboard()
        showContributionModal.value = false
        goalToContribute.value = null
      } catch (err) {
        console.error('Failed to contribute:', err)
      }
    }

    // Dashboard loading
    async function loadDashboard(range = 'custom', fromDate = '', toDate = '') {
      let params = {}
      // console.log(range)
      // if (range === 'custom' && fromDate && toDate) {
      //   params = { from_date: fromDate, to_date: toDate }
      // } else {
      //   params = { range }
      //   console.log("at else")
      // }
      params = { from_date: fromDate, to_date: toDate }
      const data = await fetchDashboardData(params)
      console.log(data)
      dashboard.value = data
      transactions.value = data.transactions || []
      savingsGoals.value = data.savings || []
    }

    async function selectRange(value) {
      await loadDashboard(value)
    }
    async function applyCustomRange() {
      if (!customFrom.value || !customTo.value) return
      await loadDashboard('custom', customFrom.value, customTo.value)
    }

    function addTransaction() {
      router.push('/student/addtransaction')
    }
    function editTransaction(transaction) {
      router.push({ name: 'edittransaction', params: { id: transaction.transaction_id } })
    }
    function addGoal() {
      router.push('/student/add-goal')
    }
    function editGoal(goal) {

      router.push({ name: 'EditGoal', params: { id: goal.goal_id } })
    }

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
      editTransaction,
      addGoal,
      editGoal,
      requestGoalDelete,
      cancelGoalDelete,
      confirmGoalDelete,
      showGoalDeleteConfirm,
      requestContribution,
      cancelContribution,
      confirmContribution,
      showContributionModal,
      contributionAmount
    }
  },
}
</script>

