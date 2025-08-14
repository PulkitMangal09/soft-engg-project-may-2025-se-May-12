<template>
  <div class="min-h-screen bg-gray-100 flex flex-col">
    <main class="flex-grow">
      <router-view />
    </main>

    <!-- Top Navigation -->
    <header class="fixed top-0 left-0 right-0 bg-white border-b border-gray-200 shadow-lg z-10 py-4 px-6">
      <div class="flex justify-between items-center">
        <!-- Left section: App Name -->
        <div class="text-2xl font-bold text-gray-800">GrowthGeine</div>

        <!-- Middle section: Navigation Links -->
        <nav class="hidden md:flex space-x-6">
          <router-link v-for="item in navItems" :key="item.name" :to="item.path"
            class="text-gray-600 hover:text-blue-600 transition-colors text-lg font-medium"
            active-class="text-blue-600">
            {{ item.name }}
          </router-link>
        </nav>

        <!-- Right section: User Profile -->
        <div class="flex items-center space-x-3">
          <img src="https://via.placeholder.com/40" alt="User Avatar"
            class="w-10 h-10 rounded-full object-cover border-2 border-blue-400">
          <span class="font-semibold text-gray-700">Mr. Rajnish</span>
        </div>
      </div>

      <!-- Mobile Navigation (visible on small screens) -->
      <nav class="md:hidden flex justify-around items-center mt-4">
        <router-link v-for="item in navItems" :key="item.name" :to="item.path"
          class="flex flex-col items-center justify-center text-gray-600 hover:text-blue-600 transition-colors w-full"
          active-class="text-blue-600">
          <component :is="item.icon" class="h-6 w-6 mb-1" />
          <span class="text-xs font-medium">{{ item.name }}</span>
        </router-link>
      </nav>
    </header>
  </div>
</template>

<script>
import { ref } from 'vue'
import { HomeIcon, ChartBarIcon, ListBulletIcon, CogIcon } from '@heroicons/vue/24/solid'

export default {
  name: 'ParentLayout',
  setup() {
    const navItems = ref([
      { name: 'Dashboard', path: '/parent/dashboard', icon: HomeIcon },
      { name: 'Analytics', path: '/parent/analytics', icon: ChartBarIcon },
      { name: 'Reports', path: '/parent/reports', icon: ListBulletIcon },
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
  padding-top: 64px;
  /* Height of the top nav */
}
</style>
