<template>
  <div class="p-6 space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">Parent Analytics</h1>
      <div class="flex items-center gap-3">
        <label class="text-sm text-gray-600">Child</label>
        <select v-model="selectedChildId" @change="onChildChange" class="border rounded px-3 py-2">
          <option v-for="c in children" :key="c.student_id" :value="c.student_id">
            {{ c.name || c.email || c.student_id }}
          </option>
        </select>
      </div>
    </div>

    <!-- Tasks + Assign -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="bg-white rounded shadow p-4">
        <div class="flex items-center justify-between mb-3">
          <h2 class="font-semibold">Assigned Tasks</h2>
          <button @click="refreshTasks" class="text-sm text-blue-600">Refresh</button>
        </div>
        <div v-if="loading.tasks" class="text-gray-500 text-sm">Loading tasks...</div>
        <ul v-else class="divide-y">
          <li v-for="t in pagedTasks" :key="t.task_id" class="py-3">
            <div class="flex justify-between">
              <div>
                <div class="font-medium">{{ t.title }}</div>
                <div class="text-xs text-gray-500">Due: {{ formatDate(t.due_date) }} • Status: {{ t.status }}</div>
              </div>
            </div>
          </li>
          <li v-if="!tasks.length" class="py-6 text-sm text-gray-500">No tasks yet.</li>
        </ul>
        <div v-if="tasks.length" class="flex items-center justify-between mt-3 text-sm">
          <div>Showing page {{ tasksPage }} of {{ tasksTotalPages }}</div>
          <div class="flex items-center gap-2">
            <button class="px-3 py-1 border rounded" :disabled="tasksPage <= 1"
              @click="changeTasksPage(tasksPage - 1)">Prev</button>
            <button class="px-3 py-1 border rounded" :disabled="tasksPage >= tasksTotalPages"
              @click="changeTasksPage(tasksPage + 1)">Next</button>
          </div>
        </div>
      </div>

      <div class="bg-white rounded shadow p-4">
        <h2 class="font-semibold mb-3">Assign New Task</h2>
        <form @submit.prevent="createTask" class="space-y-3">
          <input v-model="newTask.title" type="text" placeholder="Title" class="w-full border rounded px-3 py-2"
            required />
          <input v-model="newTask.due_date" type="date" class="w-full border rounded px-3 py-2" required />
          <textarea v-model="newTask.description" placeholder="Description"
            class="w-full border rounded px-3 py-2"></textarea>
          <div>
            <label class="block text-sm text-gray-600 mb-1">Category</label>
            <select v-model="newTask.category" class="w-full border rounded px-3 py-2" required>
              <option disabled value="">Select category…</option>
              <option>study</option>
              <option>chore</option>
              <option>health</option>
              <option>creative</option>
            </select>
          </div>
          <div class="flex items-center gap-2">
            <button type="submit" :disabled="creatingTask || !selectedChildId"
              class="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50">
              {{ creatingTask ? 'Assigning...' : 'Assign Task' }}
            </button>
            <div v-if="taskError" class="text-sm text-red-600">{{ taskError }}</div>
            <div v-if="taskSuccess" class="text-sm text-green-600">Task created</div>
          </div>
        </form>
      </div>
    </div>

    <!-- Finance Goals -->
    <div class="bg-white rounded shadow p-4">
      <div class="flex items-center justify-between mb-3">
        <h2 class="font-semibold">Finance Goals</h2>
        <button @click="refreshGoals" class="text-sm text-blue-600">Refresh</button>
      </div>
      <div v-if="loading.goals" class="text-gray-500 text-sm">Loading goals...</div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="g in goals" :key="g.goal_id" class="border rounded p-3">
          <div class="font-medium">{{ g.title }}</div>
          <div class="text-sm text-gray-500">Target: {{ currency(g.target_amount) }}</div>
          <div class="text-sm">Saved: {{ currency(g.saved_amount || 0) }}</div>
        </div>
        <div v-if="!goals.length" class="text-sm text-gray-500">No goals.</div>
      </div>
    </div>

    <!-- Transactions -->
    <div class="bg-white rounded shadow p-4">
      <div class="flex flex-col md:flex-row md:items-end md:justify-between gap-3 mb-3">
        <h2 class="font-semibold">Transactions</h2>
        <div class="flex flex-wrap items-center gap-2">
          <input v-model="filters.from_date" type="date" class="border rounded px-2 py-1" />
          <input v-model="filters.to_date" type="date" class="border rounded px-2 py-1" />
          <select v-model="filters.type" class="border rounded px-2 py-1">
            <option value="">All</option>
            <option>Income</option>
            <option>Expense</option>
          </select>
          <input v-model="filters.q" type="text" placeholder="Search" class="border rounded px-2 py-1" />
          <button @click="refreshTransactions" class="text-sm bg-gray-100 px-3 py-1 rounded">Apply</button>
        </div>
      </div>
      <div v-if="loading.transactions" class="text-gray-500 text-sm">Loading transactions...</div>
      <div v-else>
        <div class="overflow-x-auto">
          <table class="min-w-full text-sm">
            <thead>
              <tr class="text-left text-gray-600">
                <th class="py-2">Date</th>
                <th class="py-2">Type</th>
                <th class="py-2">Category</th>
                <th class="py-2">Note</th>
                <th class="py-2 text-right">Amount</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="tx in transactions.items" :key="tx.transaction_id" class="border-t">
                <td class="py-2">{{ formatDate(tx.transaction_date) }}</td>
                <td class="py-2">{{ tx.type }}</td>
                <td class="py-2">{{ tx.category }}</td>
                <td class="py-2">{{ tx.note }}</td>
                <td class="py-2 text-right" :class="tx.type === 'Income' ? 'text-green-600' : 'text-red-600'">
                  {{ currency(tx.amount) }}
                </td>
              </tr>
              <tr v-if="!transactions.items.length">
                <td colspan="5" class="py-6 text-center text-gray-500">No transactions</td>
              </tr>
            </tbody>
            <tfoot v-if="transactions.items.length" class="border-t">
              <tr>
                <td colspan="4" class="py-2 text-right font-medium">Income</td>
                <td class="py-2 text-right text-green-700 font-medium">{{ currency(totals.income) }}</td>
              </tr>
              <tr>
                <td colspan="4" class="py-2 text-right font-medium">Expense</td>
                <td class="py-2 text-right text-red-700 font-medium">{{ currency(totals.expense) }}</td>
              </tr>
              <tr>
                <td colspan="4" class="py-2 text-right font-semibold">Balance</td>
                <td class="py-2 text-right font-semibold">{{ currency(totals.income - totals.expense) }}</td>
              </tr>
            </tfoot>
          </table>
        </div>

        <div class="flex items-center justify-between mt-3 text-sm">
          <div>Showing {{ transactions.items.length }} of {{ transactions.total }}</div>
          <div class="flex items-center gap-2">
            <button class="px-3 py-1 border rounded" :disabled="transactions.page <= 1"
              @click="changePage(transactions.page - 1)">Prev</button>
            <span>Page {{ transactions.page }}</span>
            <button class="px-3 py-1 border rounded"
              :disabled="transactions.page * transactions.limit >= transactions.total"
              @click="changePage(transactions.page + 1)">Next</button>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import { parentAnalyticsService } from '@/services/parentAnalyticsService'

export default {
  name: 'ParentAnalyticsView',
  data() {
    return {
      children: [],
      selectedChildId: '',
      tasks: [],
      goals: [],
      transactions: { items: [], page: 1, limit: 20, total: 0 },
      filters: { from_date: '', to_date: '', type: '', q: '' },
      newTask: { title: '', due_date: '', description: '', category: '' },
      tasksPage: 1,
      tasksPerPage: 5,
      creatingTask: false,
      taskError: '',
      taskSuccess: false,
      loading: { tasks: false, goals: false, transactions: false, children: false },
    }
  },
  computed: {
    token() {
      return this.$store.getters['auth/token']
    },
    pagedTasks() {
      const start = (this.tasksPage - 1) * this.tasksPerPage
      return this.tasks.slice(start, start + this.tasksPerPage)
    },
    tasksTotalPages() {
      return Math.max(1, Math.ceil((this.tasks?.length || 0) / this.tasksPerPage))
    },
    totals() {
      const inc = this.transactions.items.filter(x => x.type === 'Income').reduce((s, x) => s + Number(x.amount || 0), 0)
      const exp = this.transactions.items.filter(x => x.type === 'Expense').reduce((s, x) => s + Number(x.amount || 0), 0)
      return { income: inc, expense: exp }
    }
  },
  created() {
    this.initDates()
    this.loadChildren()
  },
  methods: {
    formatDate(d) {
      if (!d) return '-'
      const dt = new Date(d)
      return isNaN(dt) ? d : dt.toLocaleDateString()
    },
    currency(v) {
      const n = Number(v || 0)
      return n.toLocaleString(undefined, { style: 'currency', currency: 'INR' })
    },
    initDates() {
      const now = new Date()
      const first = new Date(now.getFullYear(), now.getMonth(), 1)
      const fmt = (x) => x.toISOString().slice(0, 10)
      this.filters.from_date = fmt(first)
      this.filters.to_date = fmt(now)
    },
    async loadChildren() {
      try {
        this.loading.children = true
        const data = await parentAnalyticsService.getDashboard(this.token)
        this.children = data.children || []
        if (this.children.length && !this.selectedChildId) {
          this.selectedChildId = this.children[0].student_id
          await this.reloadAll()
        }
      } finally {
        this.loading.children = false
      }
    },
    async reloadAll() {
      await Promise.all([
        this.refreshTasks(),
        this.refreshGoals(),
        this.refreshTransactions(),
      ])
    },
    async onChildChange() {
      this.transactions.page = 1
      await this.reloadAll()
    },
    async refreshTasks() {
      if (!this.selectedChildId) return
      this.loading.tasks = true
      try {
        const data = await parentAnalyticsService.getTasks(this.token, { child_id: this.selectedChildId })
        this.tasks = Array.isArray(data) ? data : []
        this.tasksPage = 1
      } finally {
        this.loading.tasks = false
      }
    },
    changeTasksPage(p) {
      if (p < 1 || p > this.tasksTotalPages) return
      this.tasksPage = p
    },
    async refreshGoals() {
      if (!this.selectedChildId) return
      this.loading.goals = true
      try {
        const data = await parentAnalyticsService.getGoals(this.token, { child_id: this.selectedChildId })
        this.goals = Array.isArray(data) ? data : []
      } finally {
        this.loading.goals = false
      }
    },
    async refreshTransactions() {
      if (!this.selectedChildId) return
      this.loading.transactions = true
      try {
        const params = { child_id: this.selectedChildId, page: this.transactions.page, limit: this.transactions.limit, ...this.filters }
        const data = await parentAnalyticsService.getTransactions(this.token, params)
        this.transactions = data || { items: [], page: 1, limit: 20, total: 0 }
      } finally {
        this.loading.transactions = false
      }
    },
    async changePage(p) {
      this.transactions.page = p
      await this.refreshTransactions()
    },
    async createTask() {
      if (!this.selectedChildId) return
      this.creatingTask = true
      this.taskError = ''
      this.taskSuccess = false
      try {
        const payload = {
          title: this.newTask.title,
          description: this.newTask.description,
          due_date: this.newTask.due_date,
          category: this.newTask.category,
          assigned_to: this.selectedChildId,
        }
        await parentAnalyticsService.createTask(this.token, payload)
        this.taskSuccess = true
        this.newTask = { title: '', due_date: '', description: '', category: '' }
        await this.refreshTasks()
      } catch (e) {
        this.taskError = e?.response?.data?.detail || e.message || 'Failed to create task'
      } finally {
        this.creatingTask = false
      }
    },
  }
}
</script>

<style scoped></style>
