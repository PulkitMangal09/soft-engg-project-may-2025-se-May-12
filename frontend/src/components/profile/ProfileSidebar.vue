<template>
  <div class="fixed inset-0 z-50 overflow-hidden">
    <!-- Overlay -->
    <div 
      class="absolute inset-0 bg-black bg-opacity-50 transition-opacity"
      @click="$emit('close')"
    ></div>
    
    <!-- Sidebar -->
    <div class="fixed inset-y-0 right-0 w-4/5 max-w-sm bg-white shadow-xl">
      <div class="h-full flex flex-col">
        <!-- Close Button -->
        <div class="flex justify-end p-4">
          <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Navigation -->
        <nav class="flex-1 px-6 space-y-6">
          <!-- Mood Insights -->
          <div>
            <h3 class="text-sm font-medium text-gray-500 uppercase tracking-wider mb-3 px-2">Mood Insights</h3>
            <div class="space-y-1">
              <button 
                v-for="item in moodInsights" 
                :key="item.name"
                @click="navigateTo(item.href)"
                class="w-full flex items-center px-3 py-3 text-base font-medium rounded-lg hover:bg-gray-50"
              >
                <span :class="[item.icon, 'mr-3 text-gray-500 text-xl']"></span>
                <span>{{ item.name }}</span>
              </button>
            </div>
          </div>

          <!-- Privacy Settings -->
          <div>
            <h3 class="text-sm font-medium text-gray-500 uppercase tracking-wider mb-3 px-2">Privacy Settings</h3>
            <div class="space-y-1">
              <button 
                v-for="item in privacySettings" 
                :key="item.name"
                @click="navigateTo(item.href)"
                class="w-full flex items-center px-3 py-3 text-base font-medium rounded-lg hover:bg-gray-50"
              >
                <span :class="[item.icon, 'mr-3 text-gray-500 text-xl']"></span>
                <span>{{ item.name }}</span>
              </button>
            </div>
          </div>

          <!-- Support Options -->
          <div class="mt-6">
            <h3 class="px-4 text-sm font-medium text-gray-500 mb-2">SUPPORT</h3>
            <nav class="space-y-1">
              <a v-for="item in supportOptions" :key="item.name" :href="item.href"
                class="group flex items-center px-4 py-3 text-sm font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-900">
                <span class="mr-3 text-lg">{{ item.icon }}</span>
                {{ item.name }}
              </a>
            </nav>
          </div>

          <!-- Logout Button -->
          <div class="mt-auto pt-4 border-t border-gray-200">
            <button @click="handleLogout"
              class="w-full flex items-center justify-center px-4 py-3 text-sm font-medium text-red-600 hover:bg-red-50">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Sign out
            </button>
          </div>
        </nav>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const emit = defineEmits(['close']);
const router = useRouter();

// Mock user data - replace with actual user data from your auth store
const user = ref({
  name: 'Alex Johnson',
  email: 'alex@example.com'
});

const userName = computed(() => user.value.name);
const userInitials = computed(() => 
  user.value.name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .substring(0, 2)
);

const moodInsights = [
  { name: 'Mood History', href: '/student/insights/mood', icon: '📊' },
];

const privacySettings = [
  { name: 'Account Settings', href: '/student/settings/account', icon: '⚙️' },
  { name: 'Privacy Controls', href: '/student/settings/privacy', icon: '🔒' },
  { name: 'Notification Preferences', href: '/student/settings/notifications', icon: '🔔' },
];

const supportOptions = [
  { name: 'Help Center', href: '/student/support/help', icon: '❓' },
  { name: 'Contact Support', href: '/student/support/contact', icon: '✉️' },
  { name: 'About', href: '/about', icon: 'ℹ️' },
];

const handleLogout = () => {
  // In a real app, this would sign the user out
  console.log('Signing out...');
  emit('close');
  router.push('/login');
};

const navigateTo = (path) => {
  emit('close');
  router.push(path);
};
</script>
