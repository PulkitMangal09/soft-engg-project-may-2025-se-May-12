<template>
  <div class="min-h-screen bg-gray-100 p-4">
    <StudentNavBar />

    <div class="max-w-4xl mx-auto space-y-8">
      <div class="flex flex-col md:flex-row md:items-center justify-between mt-4 mb-8">
        <div>
          <h1 class="text-3xl font-extrabold text-gray-900">Task Manager</h1>
          <p class="text-gray-500 mt-1">Stay organized and productive.</p>
        </div>
        <div class="mt-4 md:mt-0 flex items-center space-x-4">
          <span class="text-sm font-medium text-gray-700">🏆 Points: {{ totalRewardPoints }}</span>
          <span class="text-sm font-medium text-gray-700">✅ Completed: {{ completedTaskCount }}</span>
        </div>
      </div>

<div class="bg-white rounded-xl shadow p-8 mb-10 space-y-6">
  <h2 class="text-2xl font-bold text-gray-900">Create a New Task</h2>

  <!-- Title & Description -->
  <div class="space-y-4">
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Title</label>
      <input
        v-model="newTask.title"
        type="text"
        placeholder="Enter task title"
        class="w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-blue-500 focus:border-blue-500"
      />
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Description (Optional)</label>
      <textarea
        v-model="newTask.description"
        rows="3"
        placeholder="Add additional details..."
        class="w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
      ></textarea>
    </div>
  </div>

  <!-- Category & Priority -->
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
      <select
        v-model="newTask.category"
        class="w-full border border-gray-300 rounded-md px-4 py-2 bg-white focus:ring-blue-500 focus:border-blue-500"
      >
        <option disabled value="">Select category…</option>
        <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
      </select>
    </div>
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Priority</label>
      <select
        v-model="newTask.priority"
        class="w-full border border-gray-300 rounded-md px-4 py-2 bg-white focus:ring-blue-500 focus:border-blue-500"
      >
        <option disabled value="">Select priority…</option>
        <option v-for="p in priorities" :key="p" :value="p">{{ p }}</option>
      </select>
    </div>
  </div>

  <!-- Due Date & Time -->
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
      <input
        v-model="newTask.due_date"
        type="date"
        class="w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-blue-500 focus:border-blue-500"
      />
    </div>
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Due Time</label>
      <input
        v-model="newTask.due_time"
        type="time"
        class="w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-blue-500 focus:border-blue-500"
      />
    </div>
  </div>

  <!-- Reward Points & Attachment -->
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Reward Points</label>
      <input
        v-model.number="newTask.reward_points"
        type="number"
        min="0"
        class="w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-blue-500 focus:border-blue-500"
      />
    </div>
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Attachment URL</label>
      <input
        v-model="newTask.attachment_url"
        type="url"
        placeholder="https://..."
        class="w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-blue-500 focus:border-blue-500"
      />
    </div>
  </div>

  <!-- Footer Actions -->
  <div class="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0 pt-4 border-t border-gray-200">
    <label class="inline-flex items-center text-sm text-gray-700">
      <input
        type="checkbox"
        v-model="newTask.status"
        true-value="completed"
        false-value="pending"
        class="form-checkbox h-5 w-5 text-blue-600 rounded-md mr-2"
      />
      Mark as completed
    </label>
    <button
      @click="addTask"
      class="px-6 py-2 bg-blue-600 text-white rounded-md font-semibold hover:bg-blue-700 transition"
    >
      + Add Task
    </button>
  </div>
</div>


      <div class="space-y-6">
<div class="flex flex-wrap items-center gap-3">
  <span class="text-sm font-medium text-gray-600">View:</span>

  <button
    @click="selectedFilter = 'all'"
    :class="[
      selectedFilter === 'all' 
        ? 'bg-blue-600 text-white' 
        : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
      'px-4 py-1.5 rounded-full text-sm font-medium transition'
    ]"
  >
    All
  </button>

  <button
    @click="selectedFilter = 'pending'"
    :class="[
      selectedFilter === 'pending' 
        ? 'bg-blue-600 text-white' 
        : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
      'px-4 py-1.5 rounded-full text-sm font-medium transition'
    ]"
  >
    Pending
  </button>

  <button
    @click="selectedFilter = 'completed'"
    :class="[
      selectedFilter === 'completed' 
        ? 'bg-blue-600 text-white' 
        : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
      'px-4 py-1.5 rounded-full text-sm font-medium transition'
    ]"
  >
    Completed
  </button>
</div>


        <div class="space-y-4">
          <div v-if="filteredTasks.length === 0" class="text-center py-12 text-gray-400">
            No tasks found. Get started by adding a new one!
          </div>

          <div v-for="task in filteredTasks" :key="task.__uuid"
            class="relative bg-white rounded-2xl shadow-md p-5 flex items-center group">
            <div :class="{
              'bg-green-500': task.status === 'completed',
              'bg-yellow-400': task.status === 'pending',
              'bg-red-500': task.priority === 'high'
            }" class="absolute left-0 top-0 h-full w-2 rounded-l-2xl"></div>

            <div class="flex-1 ml-4 space-y-1">
              <h3 :class="{ 'line-through text-gray-400': task.status === 'completed' }"
                class="text-lg font-semibold text-gray-800">{{ task.title }}</h3>
              <p v-if="task.description" class="text-sm text-gray-500">{{ task.description }}</p>
              <div class="text-xs text-gray-400 flex items-center space-x-4 mt-2">
                <span v-if="task.due_date">📅 {{ formatDate(task.due_date) }}</span>
                <span v-if="task.category">📂 {{ task.category }}</span>
                <span v-if="task.reward_points > 0">🎁 {{ task.reward_points }} pts</span>
              </div>
            </div>

            <div class="flex space-x-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
              <button @click="toggleTask(task)"
                class="p-2 rounded-full text-gray-500 hover:text-blue-600 hover:bg-blue-100 transition">
                <svg v-if="task.status === 'completed'" class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                  <path
                    d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
                </svg>
                <svg v-else class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z" />
                </svg>
              </button>
              <button @click="deleteTask(task)"
                class="p-2 rounded-full text-gray-500 hover:text-red-600 hover:bg-red-100 transition">
                <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                  <path
                    d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import axios from 'axios'
import StudentNavBar from '@/components/layout/StudentNavBar.vue'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

const isModalOpen = ref(false)
const currentTab = ref('details')

// Vuex + axios + auth
const store = useStore()
// Use global axios instance with authentication handled by global interceptor
const API = axios

// Reactive state
const tasks = ref([])
const selectedFilter = ref('all')
const selectedTeacher = ref('all')
const newTask = ref({
  title: '',
  description: '',
  category: '',
  priority: '',
  due_date: '',
  due_time: '',
  status: 'pending',
  reward_points: 0,
  attachment_url: ''
})

// Mock connected teachers data - in real app, this would come from API
const connectedTeachers = ref([
  {
    id: 1,
    name: 'Mrs. Johnson',
    subject: 'Mathematics',
    avatar: 'https://randomuser.me/api/portraits/women/44.jpg'
  },
  {
    id: 2,
    name: 'Mr. Smith',
    subject: 'Science',
    avatar: 'https://randomuser.me/api/portraits/men/32.jpg'
  }
])

// Dropdown values
const categories = ['homework', 'project', 'study', 'personal', 'chore', 'health', 'financial']
const priorities = ['low', 'medium', 'high']

// Computed properties
const filteredTasks = computed(() => {
  let filtered = tasks.value

  if (selectedFilter.value === 'personal') {
    // Personal: self-assigned tasks
    filtered = filtered.filter(task => String(task.assigned_by) === String(task.assigned_to))
  } else if (selectedFilter.value === 'teacher') {
    // Teacher: tasks assigned by a teacher
    filtered = filtered.filter(task => String(task.assigned_by_user_type).toLowerCase() === 'teacher')
    if (selectedTeacher.value !== 'all') {
      const teacher = connectedTeachers.value.find(t => t.id === parseInt(selectedTeacher.value))
      if (teacher) {
        // When we have names, try to match by assigned_by_name fallback to task.teacher if present
        filtered = filtered.filter(task => (task.assigned_by_name && task.assigned_by_name === teacher.name) || (task.teacher && task.teacher === teacher.name))
      }
    }
  } else if (selectedFilter.value === 'parent') {
    // Parent: tasks assigned by a parent
    filtered = filtered.filter(task => String(task.assigned_by_user_type).toLowerCase() === 'parent')
  } else if (selectedFilter.value === 'pending') {
    filtered = filtered.filter(task => task.status === 'pending')
  } else if (selectedFilter.value === 'completed') {
    filtered = filtered.filter(task => task.status === 'completed')
  }

  return filtered
})

const totalRewardPoints = computed(() => {
  return tasks.value
    .filter(task => task.status === 'completed')
    .reduce((sum, task) => sum + task.reward_points, 0)
})

const completedTaskCount = computed(() => {
  return tasks.value.filter(task => task.status === 'completed').length
})

const totalTeacherTasks = computed(() => {
  return tasks.value.filter(task => task.teacher).length
})

// Normalize each row so it always gets a unique __uuid, plus .id & .task_id
function normalizeRow(row) {
  const uuid = row?.task_id ?? row?.id ?? row?.ID
  // Spread row first, then override with normalized IDs to avoid being overwritten
  return { ...row, __uuid: uuid, task_id: uuid, id: uuid }
}

// Load tasks
onMounted(async () => {
  try {
    const { data } = await API.get('/student/tasks/')
    console.log('📬 Raw tasks:', data)
    tasks.value = data.map(normalizeRow)
  } catch {
    toast.error('Could not load tasks')
  }
})

// Helpers
function formatDate(iso) {
  return new Date(iso).toLocaleDateString(undefined, {
    month: 'short', day: 'numeric', year: 'numeric'
  })
}

// Create
async function addTask() {
  if (!newTask.value.title || !newTask.value.category || !newTask.value.priority) {
    return toast.error('Title, category & priority required')
  }
  const payload = { ...newTask.value }
  for (const k of ['description', 'due_date', 'due_time', 'attachment_url']) {
    if (!payload[k]) delete payload[k]
  }

  try {
    const { data } = await API.post('/student/tasks/', payload)
    tasks.value.push(normalizeRow(data))
    Object.assign(newTask.value, {
      title: '', description: '', category: '',
      priority: '', due_date: '', due_time: '',
      status: 'pending', reward_points: 0, attachment_url: ''
    })
    toast.success('Task added!')
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Add failed')
  }
}

// Toggle
async function toggleTask(task) {
  try {
    const { data } = await API.patch(`/student/tasks/${task.task_id}`, {
      status: task.status === 'completed' ? 'pending' : 'completed'
    })
    Object.assign(task, normalizeRow(data))
    toast.success('Status updated!')
  } catch {
    toast.error('Update failed')
  }
}

// Delete
async function deleteTask(task) {
  try {
    await API.delete(`/student/tasks/${task.task_id}`)
    tasks.value = tasks.value.filter(t => t.__uuid !== task.__uuid)
    toast.success('Task deleted!')
  } catch {
    toast.error('Delete failed')
  }
}
</script>
