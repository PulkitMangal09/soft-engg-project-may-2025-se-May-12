<template>
  <div class="bg-gray-100 font-sans p-4 md:p-6">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Manage Tasks</h1>
      <AppButton label="+ Assign New Task" variant="primary" @click="goToAssignTask" />
    </div>

    <!-- Filters -->
    <div class="flex space-x-2 mb-6 border-b border-gray-200 pb-3">
      <button 
        v-for="filter in filters" 
        :key="filter"
        @click="activeFilter = filter"
        :class="['px-4 py-2 text-sm font-semibold rounded-full', activeFilter === filter ? 'bg-blue-600 text-white' : 'bg-white text-gray-700']"
      >
        {{ filter }} ({{ filteredTasks.length }})
      </button>
    </div>

    <!-- Task List -->
    <div class="space-y-4">
      <AppCard v-for="task in filteredTasks" :key="task.id" :class="statusBorder(task.status)">
        <div class="flex flex-col md:flex-row md:justify-between">
          <!-- Task Info -->
          <div class="flex-grow mb-4 md:mb-0">
            <div class="flex items-center mb-2">
                <span :class="['px-2 py-0.5 text-xs font-semibold rounded-full mr-3', statusBackground(task.status)]">{{ task.status }}</span>
                <h3 class="text-lg font-bold text-gray-800">{{ task.title }}</h3>
            </div>
            <div class="flex items-center text-sm text-gray-500 mb-2">
                <img :src="task.assignee.avatar" class="w-6 h-6 rounded-full mr-2 object-cover">
                <span>Assigned to {{ task.assignee.name }}</span>
            </div>
            <p class="text-sm text-gray-600"><strong>Due:</strong> {{ task.dueDate }}</p>
            <p class="text-sm text-gray-600"><strong>Priority:</strong> {{ task.priority }}</p>
            <p class="text-sm text-gray-600"><strong>Reward:</strong> {{ task.rewardPoints }} points</p>
          </div>
          <!-- Actions -->
          <div class="flex flex-col md:items-end md:justify-between space-y-2">
             <div class="flex space-x-2 justify-end">
                <AppButton label="Edit" variant="secondary" size="sm" />
                <AppButton v-if="task.status !== 'Completed'" label="Mark as Complete" variant="success" size="sm" />
             </div>
          </div>
        </div>
      </AppCard>
      <div v-if="filteredTasks.length === 0" class="text-center py-8">
          <p class="text-gray-500">No tasks found for this filter.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import AppCard from '@/components/ui/AppCard.vue'
import AppButton from '@/components/ui/AppButton.vue'

export default {
  name: 'ParentTasksView',
  components: {
    AppCard,
    AppButton,
  },
  setup() {
    const router = useRouter()
    const filters = ['All', 'Pending', 'Overdue', 'Completed']
    const activeFilter = ref('All')

    const tasks = ref([
      { id: 1, title: 'Complete Math Homework', assignee: { name: 'John Jr.', avatar: 'https://randomuser.me/api/portraits/men/75.jpg' }, dueDate: '2025-07-10', priority: 'High', rewardPoints: 50, status: 'Pending' },
      { id: 2, title: 'Clean Your Room', assignee: { name: 'Emma', avatar: 'https://randomuser.me/api/portraits/women/75.jpg' }, dueDate: '2025-07-05', priority: 'Medium', rewardPoints: 30, status: 'Overdue' },
      { id: 3, title: 'Practice Piano for 30 mins', assignee: { name: 'Sophie', avatar: 'https://randomuser.me/api/portraits/women/76.jpg' }, dueDate: '2025-07-08', priority: 'Medium', rewardPoints: 20, status: 'Completed' },
      { id: 4, title: 'Read a book chapter', assignee: { name: 'John Jr.', avatar: 'https://randomuser.me/api/portraits/men/75.jpg' }, dueDate: '2025-07-12', priority: 'Low', rewardPoints: 15, status: 'Pending' },
    ])

    const filteredTasks = computed(() => {
      if (activeFilter.value === 'All') return tasks.value
      return tasks.value.filter(task => task.status === activeFilter.value)
    })

    const statusClasses = {
        'Pending': { border: 'border-l-4 border-blue-500', bg: 'bg-blue-100 text-blue-800' },
        'Overdue': { border: 'border-l-4 border-red-500', bg: 'bg-red-100 text-red-800' },
        'Completed': { border: 'border-l-4 border-green-500', bg: 'bg-green-100 text-green-800' },
    }

    function statusBorder(status) {
        return statusClasses[status]?.border || 'border-l-4 border-gray-300'
    }

    function statusBackground(status) {
        return statusClasses[status]?.bg || 'bg-gray-100 text-gray-800'
    }

    function goToAssignTask() {
        router.push({ name: 'ParentAssignTask' })
    }

    return {
      filters,
      activeFilter,
      tasks,
      filteredTasks,
      statusBorder,
      statusBackground,
      goToAssignTask
    }
  },
}
</script>
