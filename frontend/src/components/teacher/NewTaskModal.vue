<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black/30 flex items-center justify-center z-50">
    <div class="bg-white w-full max-w-xl rounded-2xl shadow-xl p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="font-semibold text-lg">Create Task</h3>
        <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700">✖</button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="md:col-span-2">
          <label class="block text-sm text-gray-600 mb-1">Title</label>
          <input v-model="form.title" type="text" class="w-full border rounded-lg px-3 py-2" />
        </div>

        <div class="md:col-span-2">
          <label class="block text-sm text-gray-600 mb-1">Description</label>
          <textarea v-model="form.description" rows="2" class="w-full border rounded-lg px-3 py-2"></textarea>
        </div>

        <div>
          <label class="block text-sm text-gray-600 mb-1">Category</label>
          <select v-model="form.category" class="w-full border rounded-lg px-3 py-2">
            <option disabled value="">Select…</option>
            <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
          </select>
        </div>

        <div>
          <label class="block text-sm text-gray-600 mb-1">Priority</label>
          <select v-model="form.priority" class="w-full border rounded-lg px-3 py-2">
            <option disabled value="">Select…</option>
            <option v-for="p in priorities" :key="p" :value="p">{{ p }}</option>
          </select>
        </div>

        <div>
          <label class="block text-sm text-gray-600 mb-1">Due Date</label>
          <input v-model="form.due_date" type="date" class="w-full border rounded-lg px-3 py-2" />
        </div>

        <div>
          <label class="block text-sm text-gray-600 mb-1">Due Time</label>
          <input v-model="form.due_time" type="time" class="w-full border rounded-lg px-3 py-2" />
        </div>

        <div>
          <label class="block text-sm text-gray-600 mb-1">Reward Points</label>
          <input v-model.number="form.reward_points" type="number" min="0" class="w-full border rounded-lg px-3 py-2" />
        </div>

        <div>
          <label class="block text-sm text-gray-600 mb-1">Attachment URL</label>
          <input v-model="form.attachment_url" type="url" class="w-full border rounded-lg px-3 py-2" />
        </div>

        <div class="md:col-span-2">
          <label class="block text-sm text-gray-600 mb-1">Assign to (student email)</label>
          <input v-model="form.assigned_to_email" type="email" class="w-full border rounded-lg px-3 py-2" placeholder="student@example.com" />
        </div>
      </div>

      <div class="mt-6 flex justify-end gap-3">
        <button @click="$emit('close')" class="px-4 py-2 rounded-lg bg-gray-100 text-gray-700 hover:bg-gray-200">Cancel</button>
        <button @click="createTask" class="px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700">Create</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useStore } from 'vuex'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

const props = defineProps({
  isOpen: { type: Boolean, default: false }
})
const emit = defineEmits(['close', 'created'])

const store = useStore()

function getAuthHeader() {
  const stored = store.state?.auth?.token || localStorage.getItem('token') || ''
  if (!stored) return null
  const raw = stored.replace(/^bearer\s+/i, '').replace(/^Bearer\s+/, '')
  return `Bearer ${raw}`
}

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
})

API.interceptors.request.use(cfg => {
  const authHeader = getAuthHeader()
  if (authHeader) cfg.headers.Authorization = authHeader
  return cfg
})

const categories = ['homework', 'project', 'study', 'personal', 'chore', 'health', 'financial']
const priorities = ['low', 'medium', 'high']

const form = ref({
  title: '',
  description: '',
  category: '',
  priority: '',
  due_date: '',
  due_time: '',
  status: 'pending',
  reward_points: 0,
  attachment_url: '',
  assigned_to_email: ''
})

async function createTask() {
  if (!form.value.title || !form.value.category || !form.value.priority || !form.value.assigned_to_email) {
    toast.error('Title, category, priority, and assigned_to_email are required')
    return
  }
  const payload = { ...form.value }

  if (payload.due_date) {
    const d = new Date(payload.due_date + 'T00:00:00')
    payload.due_date = d.toISOString()
  }
  if (!payload.due_time) delete payload.due_time
  if (!payload.attachment_url) delete payload.attachment_url
  if (!payload.description) delete payload.description
  delete payload.assigned_to

  try {
    await API.post('/teacher/tasks/', payload)
    toast.success('Task created')
    // reset form
    Object.assign(form.value, {
      title: '', description: '', category: '', priority: '',
      due_date: '', due_time: '', status: 'pending',
      reward_points: 0, attachment_url: '', assigned_to_email: ''
    })
    emit('created')
    emit('close')
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Create failed')
  }
}
</script>
