<!-- Emotion view.vue -->

<template>
  <div class="min-h-screen bg-gradient-to-b from-slate-50 to-white">
    <!-- navbar -->
    <StudentNavBar />

    <!-- Hero -->
    <header class="max-w-6xl mx-auto px-4 pt-6">
      <div
        class="bg-gradient-to-r from-indigo-500 via-violet-500 to-pink-500 text-white rounded-2xl p-5 shadow-xl flex flex-col md:flex-row items-center gap-4 md:gap-6"
      >
        <div class="flex items-center gap-4">
          <!-- mascot circle -->
          <div class="w-20 h-20 rounded-full bg-white/25 flex items-center justify-center text-4xl shadow-md">
            😊
          </div>
          <div>
            <h1 class="text-2xl md:text-3xl font-extrabold leading-tight">Hello, {{ userName }} 👋</h1>
            <p class="mt-1 text-sm md:text-base opacity-95">How are you feeling today? Let’s check in — it only takes a moment.</p>
          </div>
        </div>

        <div class="ml-auto flex gap-3">
          <button
            @click="handleDailyCheckIn"
            class="inline-flex items-center gap-3 bg-white text-indigo-600 font-semibold px-4 py-2 rounded-full shadow hover:shadow-lg transform hover:-translate-y-0.5 transition"
          >
            <span class="text-xl">📝</span>
            <span>Log Mood</span>
          </button>

          <button @click="showProfile = true" class="w-10 h-10 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center">
            ☰
          </button>
        </div>
      </div>

      <!-- privacy banner -->
      <div class="mt-4 bg-yellow-50 border-l-4 border-yellow-300 text-yellow-800 rounded-xl p-3 shadow-sm flex items-start gap-3 max-w-3xl">
        <div class="text-2xl">🔒</div>
        <div class="text-sm">Your emotional data is private and secure. Parents cannot access this information.</div>
      </div>
    </header>

    <!-- Main content -->
    <main class="max-w-6xl mx-auto px-4 pb-12 space-y-6 mt-6">
      <!-- Quick actions -->
      <section>
        <h2 class="text-lg font-semibold text-slate-800 mb-3">Quick Actions</h2>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <QuickActionCard title="Log Mood" subtitle="Share how you feel" icon="📝" color="from-pink-50 to-pink-100" @click="$router.push('/student/emotion/new')" />
          <QuickActionCard title="Chat Support" subtitle="Talk to someone" icon="💬" color="from-yellow-50 to-yellow-100" @click="$router.push('/student/emotion/chat')" />
          <QuickActionCard title="Emergency Help" subtitle="Immediate help" icon="📞" color="from-red-50 to-red-100" @click="$router.push('/student/emotion/emergency')" />
          <QuickActionCard title="My Diary" subtitle="View entries" icon="📖" color="from-green-50 to-green-100" @click="$router.push('/student/diary')" />
        </div>
      </section>

      <!-- Summary + Trends row -->
      <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Mood Summary (big) -->
        <div class="lg:col-span-2">
          <MoodSummary :logs="moodLogs" />
        </div>

        <!-- Trends card -->
        <div>
          <div class="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
            <EmotionStats />
          </div>
        </div>
      </section>

      <!-- Current Mood hero
      <section>
        <div class="bg-white rounded-2xl p-8 shadow-lg border border-gray-100 text-center">
          <div class="mx-auto w-28 h-28 rounded-full bg-indigo-50 flex items-center justify-center text-6xl mb-4 shadow-sm"> 
            {{ currentMood.emoji || '😊' }}
          </div>
          <h3 :class="['text-xl font-semibold', currentMood.textColor || 'text-slate-800']">
            {{ currentMood.message || 'How are you today?' }}
          </h3>
          <p class="mt-2 text-sm text-slate-500">{{ hasCheckedInToday ? 'You checked in today — great job!' : 'Tap below to log a quick check-in.' }}</p>

          <div class="mt-6 flex justify-center">
            <button
              @click="handleDailyCheckIn"
              :disabled="hasCheckedInToday"
              :class="[
                'px-6 py-2 rounded-full font-medium transition shadow',
                hasCheckedInToday ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-indigo-600 text-white hover:bg-indigo-700'
              ]"
            >
              {{ hasCheckedInToday ? 'Checked In' : 'Log Daily Check-in' }}
            </button>
          </div>
        </div>
      </section> -->
    </main>

    <ProfileSidebar v-if="showProfile" @close="showProfile = false" />
  </div>
</template>

<script setup>
import StudentNavBar from '@/components/layout/StudentNavBar.vue'
import ProfileSidebar from '@/components/profile/ProfileSidebar.vue'
import QuickActionCard from '@/components/emotions/QuickActionCard.vue'
import MoodSummary from '@/components/emotions/MoodSummary.vue'
import EmotionStats from '@/components/emotions/EmotionStats.vue'
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { listMoodLogs } from '@/services/moodService'

const store = useStore()
const userName = computed(() => store.getters['auth/currentUser']?.name || 'Student')

const showProfile = ref(false)
const router = useRouter()

const lastCheckIn = ref(localStorage.getItem('lastCheckIn') || null)
const currentMood = ref(JSON.parse(localStorage.getItem('currentMood')) || {})

const hasCheckedInToday = computed(() => {
  if (!lastCheckIn.value) return false
  const last = new Date(lastCheckIn.value)
  const today = new Date()
  return last.toDateString() === today.toDateString()
})

const handleDailyCheckIn = () => router.push('/student/emotion/new')

const updateMoodDisplay = () => {
  const moodData = JSON.parse(localStorage.getItem('lastMoodEntry') || '{}')
  if (moodData && moodData.mood) {
    const map = {
      happy: { emoji: '😊', message: 'Feeling Good Today!', textColor: 'text-green-600' },
      sad: { emoji: '😢', message: 'Feeling a Bit Down', textColor: 'text-blue-600' },
      angry: { emoji: '😠', message: 'Feeling Frustrated', textColor: 'text-red-600' },
      anxious: { emoji: '😰', message: 'Feeling Anxious', textColor: 'text-amber-600' },
      excited: { emoji: '🎉', message: 'Feeling Excited!', textColor: 'text-pink-600' }
    }
    currentMood.value = map[moodData.mood] || { emoji: '😊', message: 'How are you today?', textColor: 'text-slate-800' }
    localStorage.setItem('currentMood', JSON.stringify(currentMood.value))
  }
}

const moodLogs = ref([])
onMounted(async () => {
  updateMoodDisplay()
  window.addEventListener('moodUpdated', updateMoodDisplay)
  try {
    moodLogs.value = await listMoodLogs()
  } catch (e) {
    moodLogs.value = []
  }
})
</script>
