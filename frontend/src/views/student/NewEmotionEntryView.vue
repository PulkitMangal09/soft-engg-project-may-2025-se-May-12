<template>
  <div class="min-h-screen bg-gray-50">
    <StudentNavBar />
    <div class="p-4 max-w-md mx-auto">
      <div class="flex items-center mb-6">
        <router-link to="/student/emotion" class="mr-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </router-link>
        <h1 class="text-2xl font-bold">New Mood Entry</h1>
      </div>

      <form @submit.prevent="submitEntry">
        <div class="mb-6">
          <MoodSelector v-model="form.mood" />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Energy level</label>
            <select v-model="form.energy_level" class="w-full border rounded-lg px-3 py-2">
              <option :value="null">Select…</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Sleep quality</label>
            <select v-model="form.sleep_quality" class="w-full border rounded-lg px-3 py-2">
              <option :value="null">Select…</option>
              <option value="poor">Poor</option>
              <option value="fair">Fair</option>
              <option value="great">Great</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Stress level</label>
            <select v-model="form.stress_level" class="w-full border rounded-lg px-3 py-2">
              <option :value="null">Select…</option>
              <option value="relaxed">Relaxed</option>
              <option value="moderate">Moderate</option>
              <option value="high">High</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Date</label>
            <input type="date" v-model="form.log_date" class="w-full border rounded-lg px-3 py-2" />
          </div>
        </div>

        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">Notes (optional)</label>
          <textarea v-model="form.notes" rows="4"
            class="w-full p-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
            placeholder="Describe your feelings, what happened today..."></textarea>
        </div>

        <button type="submit"
          class="w-full bg-blue-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-blue-700 transition-colors">
          Log Mood
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import StudentNavBar from '@/components/layout/StudentNavBar.vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import MoodSelector from '@/components/emotions/MoodSelector.vue'
import { createMoodLog } from '@/services/moodService'

const router = useRouter()

const today = new Date().toISOString().slice(0, 10)
const form = ref({
  mood: 'neutral',
  energy_level: null,
  sleep_quality: null,
  stress_level: null,
  notes: '',
  log_date: today
})

async function submitEntry() {
  await createMoodLog({ ...form.value })
  router.push('/student/emotion')
}
</script>
