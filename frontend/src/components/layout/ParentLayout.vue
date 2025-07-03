<template>
  <div class="min-h-screen bg-gray-100 flex flex-col">
    <main class="flex-grow">
      <router-view />
    </main>

    <!-- Bottom Navigation -->
    <footer class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-lg">
      <nav class="flex justify-around items-center h-16">
        <router-link v-for="item in navItems" :key="item.name" :to="item.path" class="flex flex-col items-center justify-center text-gray-600 hover:text-blue-600 transition-colors w-full" active-class="text-blue-600">
          <component :is="item.icon" class="h-6 w-6 mb-1" />
          <span class="text-xs font-medium">{{ item.name }}</span>
        </router-link>
      </nav>
    </footer>
  </div>
</template>

<script>
import { ref } from 'vue'
import { HomeIcon, ChartBarIcon, ClipboardListIcon, CogIcon } from '@heroicons/vue/solid'

export default {
  name: 'ParentLayout',
  components: {
    HomeIcon,
    ChartBarIcon,
    ClipboardListIcon,
    CogIcon,
  },
  setup() {
    const navItems = ref([
      { name: 'Dashboard', path: '/parent/dashboard', icon: 'HomeIcon' },
      { name: 'Analytics', path: '/parent/analytics', icon: 'ChartBarIcon' },
      { name: 'Tasks', path: '/parent/tasks', icon: 'ClipboardListIcon' },
      { name: 'Settings', path: '/parent/settings', icon: 'CogIcon' },
    ])

    return {
      navItems,
    }
  },
}
</script>

<style scoped>
/* Add a bit of padding to the bottom of the main content to prevent overlap with the fixed footer */
main {
  padding-bottom: 64px; /* Height of the bottom nav */
}
</style>
