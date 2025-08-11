<template>
  <div class="min-h-screen bg-gray-50">
    <StudentNavBar />

    <div class="p-4 max-w-3xl mx-auto">
      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-2xl font-bold text-gray-800 mb-1">Task Management</h1>
        <p class="text-gray-600">Organize your tasks and stay on top of your work</p>
      </div>

      <!-- Connection Status -->
      <div class="bg-white rounded-xl shadow-sm p-4 mb-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <span class="text-lg">👨‍🏫</span>
            <div>
              <p class="font-semibold text-gray-800">{{ connectedTeachers.length }} Teachers Connected</p>
              <p class="text-sm text-gray-500">{{ totalTeacherTasks }} tasks from teachers</p>
            </div>
          </div>
          <router-link to="/student/my-connections" class="text-blue-600 hover:underline text-sm">
            Manage Connections →
          </router-link>
        </div>
      </div>

      <!-- Task Filters -->
      <div class="bg-white rounded-xl shadow-sm p-4 mb-6">
        <div class="flex items-center space-x-4">
          <label class="text-sm font-medium text-gray-700">Filter by:</label>
          <select v-model="selectedFilter" class="border-gray-300 rounded-lg text-sm">
            <option value="all">All Tasks</option>
            <option value="personal">Personal Tasks</option>
            <option value="teacher">Teacher Tasks</option>
            <option value="pending">Pending</option>
            <option value="completed">Completed</option>
          </select>
          <select v-if="selectedFilter === 'teacher'" v-model="selectedTeacher" class="border-gray-300 rounded-lg text-sm">
            <option value="all">All Teachers</option>
            <option v-for="teacher in connectedTeachers" :key="teacher.id" :value="teacher.id">
              {{ teacher.name }}
            </option>
          </select>
        </div>
      </div>

      <!-- Create New Task Form -->
      <div class="bg-white rounded-xl shadow-sm p-6 mb-8 space-y-4">
        <h2 class="text-lg font-semibold">Create New Task</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Title -->
          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Title</label>
            <input v-model="newTask.title" type="text" placeholder="Task title"
              class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500" />
          </div>

          <!-- Description -->
          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea v-model="newTask.description" rows="2" placeholder="Optional description"
              class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500"></textarea>
          </div>

          <!-- Category -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
            <select v-model="newTask.category"
              class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500">
              <option disabled value="">Select category…</option>
              <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
            </select>
          </div>

          <!-- Priority -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Priority</label>
            <select v-model="newTask.priority"
              class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500">
              <option disabled value="">Select priority…</option>
              <option v-for="p in priorities" :key="p" :value="p">{{ p }}</option>
            </select>
          </div>

          <!-- Due Date -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
            <input v-model="newTask.due_date" type="date"
              class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500" />
          </div>

          <!-- Due Time -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Due Time</label>
            <input v-model="newTask.due_time" type="time"
              class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500" />
          </div>

          <!-- Reward Points -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Reward Points</label>
            <input v-model.number="newTask.reward_points" type="number" min="0"
              class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500" />
          </div>

          <!-- Attachment URL -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Attachment URL</label>
            <input v-model="newTask.attachment_url" type="url" placeholder="https://..."
              class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500" />
          </div>

          <!-- Status & Add -->
          <div class="md:col-span-2 flex items-center mt-2">
            <label class="inline-flex items-center">
              <input type="checkbox" v-model="newTask.status" true-value="completed" false-value="pending"
                class="form-checkbox h-5 w-5 text-blue-600" />
              <span class="ml-2 text-sm text-gray-700">Mark as completed</span>
            </label>
            <button @click="addTask"
              class="ml-auto px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
              + Add Task
            </button>
          </div>
        </div>
      </div>

      <!-- Task List -->
      <div class="space-y-4">
        <template v-if="filteredTasks.length">
          <div v-for="task in filteredTasks" :key="task.__uuid" class="bg-white rounded-xl shadow-sm p-4 flex items-start">
            <div :class="task.status === 'completed' ? 'bg-green-400' : 'bg-yellow-400'"
              class="h-3 w-3 rounded-full mt-1 mr-3"></div>

            <div class="flex-1">
              <h3 class="font-semibold text-lg">{{ task.title }}</h3>
              <p v-if="task.description" class="text-gray-600 text-sm">{{ task.description }}</p>
              <div class="mt-2 text-xs text-gray-500 space-x-4">
                <span>📂 {{ task.category }}</span>
                <span>🚩 {{ task.priority }}</span>
                <span>
                  📅 {{ task.due_date ? formatDate(task.due_date) : '—' }}
                  <span v-if="task.due_time">at {{ task.due_time }}</span>
                </span>
                <span>🎁 {{ task.reward_points }} pts</span>
                <span v-if="task.teacher" class="text-blue-600">
                  👨‍🏫 {{ task.teacher }}
                </span>
                <span v-if="task.attachment_url">
                  🔗
                  <a :href="task.attachment_url" target="_blank" class="underline">
                    Attachment
                  </a>
                </span>
              </div>
              <div v-if="task.teacher" class="mt-2 flex items-center space-x-2">
                <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  Teacher Task
                </span>
                <span class="text-xs text-gray-500">Assigned by {{ task.teacher }}</span>
              </div>
            </div>

            <div class="flex-shrink-0 flex flex-col items-center ml-4 space-y-2">
              <button @click="toggleTask(task)" title="Toggle Status" class="p-1 rounded-full hover:bg-gray-100">
                <svg v-if="task.status === 'completed'" xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5 text-green-600" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 
                       0 01-1.414 0l-4-4a1 1 0 
                       011.414-1.414L8 12.586l7.293-7.293a1 1 
                       0 011.414 0z" clip-rule="evenodd" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none"
                  viewBox="0 0 24 24" stroke="currentColor">
                  <circle cx="12" cy="12" r="9" stroke-width="2" />
                </svg>
              </button>

              <button @click="deleteTask(task)" title="Delete" class="p-1 rounded-full hover:bg-gray-100">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-red-500" viewBox="0 0 20 20"
                  fill="currentColor">
                  <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 
                       4H4a1 1 0 000 2v10a2 2 0 
                       002 2h8a2 2 0 002-2V6a1 
                       1 0 100-2h-3.382l-.724-1.447A1 
                       1 0 0011 2H9zM7 8a1 1 0 
                       012 0v6a1 1 0 11-2 0V8zm5-1a1 
                       1 0 00-1 1v6a1 1 0 102 
                       0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
        </template>

        <div v-else class="text-center py-12 text-gray-400">
          No tasks yet. Add one above!
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
    filtered = filtered.filter(task => !task.teacher)
  } else if (selectedFilter.value === 'teacher') {
    filtered = filtered.filter(task => task.teacher)
    if (selectedTeacher.value !== 'all') {
      const teacher = connectedTeachers.value.find(t => t.id === parseInt(selectedTeacher.value))
      if (teacher) {
        filtered = filtered.filter(task => task.teacher === teacher.name)
      }
    }
  } else if (selectedFilter.value === 'pending') {
    filtered = filtered.filter(task => task.status === 'pending')
  } else if (selectedFilter.value === 'completed') {
    filtered = filtered.filter(task => task.status === 'completed')
  }

  return filtered
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
