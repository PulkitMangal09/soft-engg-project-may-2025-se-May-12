<template>
  <div class="flex flex-col h-screen bg-gray-50">

    <!-- Header -->
    <div class="px-4 py-3 border-b border-gray-200 flex items-center justify-between bg-white">
      <button @click="$router.go(-1)" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100">
        ←
      </button>
      <h1 class="text-lg font-semibold">Emotion Center</h1>
      <button @click="showProfile = true" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
    </div>

    <!-- Main Content -->
    <div class="flex-1 overflow-y-auto p-4 space-y-4">
      <!-- Privacy Banner -->
      <div class="bg-blue-50 text-blue-800 text-xs p-3 rounded-lg flex items-start">
        <span class="mr-2">🔒</span>
        <span>Your emotional data is private and secure. Parents cannot access this information.</span>
      </div>

      <!-- Quick Actions -->
      <div class="grid grid-cols-4 gap-2 mb-4">
        <QuickActionCard title="Log Emotion" icon="📝" @click="$router.push('/student/emotion/new')" />
        <QuickActionCard title="Chat Support" icon="💬" @click="$router.push('/student/emotion/chat')" />
        <QuickActionCard title="Emergency Help" icon="📞" @click="$router.push('/student/emotion/emergency')" />
        <QuickActionCard title="My Diary" icon="📖" @click="$router.push('/student/diary')" />
      </div>

      <!-- Mood Trends -->
      <div class="bg-white rounded-xl p-4 shadow-sm">
        <h2 class="font-semibold text-gray-700 mb-3">This Week's Mood Trends</h2>
        <EmotionStats />
        <div class="flex justify-between text-xs text-gray-500 mt-1">
          <span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span><span>Sun</span>
        </div>
      </div>

      <!-- Current Mood -->
      <div class="text-center bg-white rounded-xl p-6 shadow-sm">
        <div class="text-5xl mb-3">{{ currentMood.emoji || '😊' }}</div>
        <div :class="['font-bold text-lg', currentMood.textColor || 'text-green-600']">
          {{ currentMood.message || 'How are you feeling today?' }}
        </div>
        <div class="text-sm text-gray-500 mb-4">
          {{ hasCheckedInToday ? 'You checked in today' : 'How are you feeling right now?' }}
        </div>
        <button @click="handleDailyCheckIn" :disabled="hasCheckedInToday" :class="[
          'px-6 py-2 rounded-full font-medium text-sm transition-all',
          hasCheckedInToday
            ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
            : 'bg-blue-600 text-white hover:bg-blue-700 shadow-md hover:shadow-lg transform hover:-translate-y-0.5'
        ]">
          {{ hasCheckedInToday ? 'Checked In' : 'Log Daily Check-in' }}
        </button>
      </div>
    </div>

    <!-- Bottom Navigation -->
    <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 flex justify-around py-2 px-4 z-40">
      <router-link 
        to="/student/tasks" 
        :class="[
          'flex flex-col items-center py-1 px-2 rounded-lg transition-colors',
          $route.path.includes('/tasks') ? 'text-blue-600 bg-blue-50' : 'text-gray-500 hover:text-blue-500'
        ]"
      >
        <span class="text-2xl">📋</span>
        <span class="text-xs mt-0.5">Tasks</span>
      </router-link>
      <router-link 
        to="/student/finance" 
        :class="[
          'flex flex-col items-center py-1 px-2 rounded-lg transition-colors',
          $route.path.includes('/finance') ? 'text-blue-600 bg-blue-50' : 'text-gray-500 hover:text-blue-500'
        ]"
      >
        <span class="text-2xl">💰</span>
        <span class="text-xs mt-0.5">Finance</span>
      </router-link>
      <router-link 
        to="/student/diet" 
        :class="[
          'flex flex-col items-center py-1 px-2 rounded-lg transition-colors',
          $route.path.includes('/diet') ? 'text-blue-600 bg-blue-50' : 'text-gray-500 hover:text-blue-500'
        ]"
      >
        <span class="text-2xl">🥗</span>
        <span class="text-xs mt-0.5">Diet</span>
      </router-link>
    </div>

    <!-- Profile Sidebar -->
    <ProfileSidebar v-if="showProfile" @close="showProfile = false" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import QuickActionCard from '@/components/emotions/QuickActionCard.vue';
import EmotionStats from '@/components/emotions/EmotionStats.vue';
import ProfileSidebar from '@/components/profile/ProfileSidebar.vue';

// Profile sidebar state
const showProfile = ref(false);

// State
const lastCheckIn = ref(localStorage.getItem('lastCheckIn') || null);
const currentMood = ref(JSON.parse(localStorage.getItem('currentMood')) || {});

// Computed
const hasCheckedInToday = computed(() => {
  if (!lastCheckIn.value) return false;
  const lastCheckInDate = new Date(lastCheckIn.value);
  const today = new Date();
  return (
    lastCheckInDate.getDate() === today.getDate() &&
    lastCheckInDate.getMonth() === today.getMonth() &&
    lastCheckInDate.getFullYear() === today.getFullYear()
  );
});

// Methods
const router = useRouter();
const handleDailyCheckIn = () => {
  router.push('/student/emotion/new');
};

// Update UI when a new mood is logged
const updateMoodDisplay = () => {
  const moodData = JSON.parse(localStorage.getItem('lastMoodEntry') || '{}');
  if (moodData) {
    currentMood.value = {
      emoji: moodData.mood === 'happy' ? '😊' :
        moodData.mood === 'sad' ? '😢' :
          moodData.mood === 'angry' ? '😠' :
            moodData.mood === 'anxious' ? '😰' :
              moodData.mood === 'excited' ? '🎉' : '😊',
      message: moodData.mood === 'happy' ? 'Feeling Good Today!' :
        moodData.mood === 'sad' ? 'Feeling a Bit Down' :
          moodData.mood === 'angry' ? 'Feeling Frustrated' :
            moodData.mood === 'anxious' ? 'Feeling Anxious' :
              moodData.mood === 'excited' ? 'Feeling Excited!' : 'How are you today?',
      textColor: moodData.mood === 'happy' ? 'text-green-600' :
        moodData.mood === 'sad' ? 'text-blue-600' :
          moodData.mood === 'angry' ? 'text-red-600' :
            moodData.mood === 'anxious' ? 'text-yellow-600' :
              moodData.mood === 'excited' ? 'text-purple-600' : 'text-gray-600'
    };
    localStorage.setItem('currentMood', JSON.stringify(currentMood.value));
  }
};

// Initialize
onMounted(() => {
  updateMoodDisplay();

  // Listen for mood updates from other components
  window.addEventListener('moodUpdated', updateMoodDisplay);

  return () => {
    window.removeEventListener('moodUpdated', updateMoodDisplay);
  };
});

// Mock data - replace with API call later
const diaryEntries = ref([
  { id: 1, mood: 'happy', text: 'Had a great day at school.', tags: ['school', 'friends'], date: '2025-07-02T10:00:00Z' },
  { id: 2, mood: 'anxious', text: 'Worried about the upcoming exam.', tags: ['exam', 'stress'], date: '2025-07-01T18:30:00Z' },
  { id: 3, mood: 'excited', text: 'Family trip this weekend!', tags: ['family', 'vacation'], date: '2025-06-30T15:00:00Z' },
  { id: 4, mood: 'sad', text: 'Missed my friends today.', tags: ['friends'], date: '2025-06-29T20:00:00Z' },
]);

const recentEntries = computed(() => diaryEntries.value.slice(0, 3));
</script>
