<template>
  <div class="min-h-screen p-6 sm:p-8 flex items-center justify-center">
    <div class="w-full max-w-2xl">
      <div class="flex items-center justify-start mb-8 lg:mb-12">
        <router-link to="/student/emotion" class="mr-4 text-gray-500 hover:text-blue-600 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </router-link>
        <h1 class="text-3xl font-bold text-gray-900">Let's check in.</h1>
      </div>

                      <div class="hidden lg:block lg:col-span-1 p-6 space-y-6">
          <div class="bg-white rounded-2xl p-6 shadow-lg border border-gray-200">
            <h3 class="text-xl font-bold text-gray-800 mb-4">Mindfulness Tip</h3>
            <p class="text-gray-600">Take a deep breath. Close your eyes and focus on the sensation of the air entering and leaving your body. Do this for 60 seconds to calm your mind.</p>
          </div>
        </div>

      <form @submit.prevent="submitEntry" class="space-y-6">
        <div class="bg-white bg-opacity-90 rounded-3xl p-8 shadow-xl border border-gray-200">
          <div>
            <label class="block text-xl font-bold text-gray-800 mb-4">Choose your mood</label>
            <MoodSelector v-model="form.mood" />
          </div>

          <hr class="my-6 border-gray-200" />
          
          <div class="space-y-5">
            <div>
              <label class="block text-lg font-semibold text-gray-700 mb-2">Energy level</label>
              <div class="flex space-x-3">
                <button type="button" @click="form.energy_level = 'low'" :class="{'bg-blue-600 text-white': form.energy_level === 'low', 'bg-gray-100 text-gray-700 hover:bg-gray-200': form.energy_level !== 'low'}" class="flex-1 py-3 rounded-xl font-medium transition-colors">Low</button>
                <button type="button" @click="form.energy_level = 'medium'" :class="{'bg-blue-600 text-white': form.energy_level === 'medium', 'bg-gray-100 text-gray-700 hover:bg-gray-200': form.energy_level !== 'medium'}" class="flex-1 py-3 rounded-xl font-medium transition-colors">Medium</button>
                <button type="button" @click="form.energy_level = 'high'" :class="{'bg-blue-600 text-white': form.energy_level === 'high', 'bg-gray-100 text-gray-700 hover:bg-gray-200': form.energy_level !== 'high'}" class="flex-1 py-3 rounded-xl font-medium transition-colors">High</button>
              </div>
            </div>

            <div>
              <label class="block text-lg font-semibold text-gray-700 mb-2">Sleep quality</label>
              <div class="flex space-x-3">
                <button type="button" @click="form.sleep_quality = 'poor'" :class="{'bg-blue-600 text-white': form.sleep_quality === 'poor', 'bg-gray-100 text-gray-700 hover:bg-gray-200': form.sleep_quality !== 'poor'}" class="flex-1 py-3 rounded-xl font-medium transition-colors">Poor</button>
                <button type="button" @click="form.sleep_quality = 'fair'" :class="{'bg-blue-600 text-white': form.sleep_quality === 'fair', 'bg-gray-100 text-gray-700 hover:bg-gray-200': form.sleep_quality !== 'fair'}" class="flex-1 py-3 rounded-xl font-medium transition-colors">Fair</button>
                <button type="button" @click="form.sleep_quality = 'great'" :class="{'bg-blue-600 text-white': form.sleep_quality === 'great', 'bg-gray-100 text-gray-700 hover:bg-gray-200': form.sleep_quality !== 'great'}" class="flex-1 py-3 rounded-xl font-medium transition-colors">Great</button>
              </div>
            </div>

            <div>
              <label class="block text-lg font-semibold text-gray-700 mb-2">Stress level</label>
              <div class="flex space-x-3">
                <button type="button" @click="form.stress_level = 'relaxed'" :class="{'bg-blue-600 text-white': form.stress_level === 'relaxed', 'bg-gray-100 text-gray-700 hover:bg-gray-200': form.stress_level !== 'relaxed'}" class="flex-1 py-3 rounded-xl font-medium transition-colors">Relaxed</button>
                <button type="button" @click="form.stress_level = 'moderate'" :class="{'bg-blue-600 text-white': form.stress_level === 'moderate', 'bg-gray-100 text-gray-700 hover:bg-gray-200': form.stress_level !== 'moderate'}" class="flex-1 py-3 rounded-xl font-medium transition-colors">Moderate</button>
                <button type="button" @click="form.stress_level = 'high'" :class="{'bg-blue-600 text-white': form.stress_level === 'high', 'bg-gray-100 text-gray-700 hover:bg-gray-200': form.stress_level !== 'high'}" class="flex-1 py-3 rounded-xl font-medium transition-colors">High</button>
              </div>
            </div>

            <div>
              <label class="block text-lg font-semibold text-gray-700 mb-2">Notes (optional)</label>
              <textarea v-model="form.notes" rows="4" class="w-full p-4 border border-gray-300 rounded-xl focus:ring-blue-500 focus:border-blue-500 transition-colors" placeholder="Describe your feelings, what happened today..."></textarea>
            </div>

            <div>
              <label class="block text-lg font-semibold text-gray-700 mb-2">Date</label>
              <input type="date" v-model="form.log_date" class="w-full p-4 border border-gray-300 rounded-xl focus:ring-blue-500 focus:border-blue-500 transition-colors" />
            </div>
          </div>
        </div>


        <button type="submit" class="w-full bg-blue-600 text-white font-bold py-4 px-4 rounded-2xl hover:bg-blue-700 transition-colors shadow-lg">
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
