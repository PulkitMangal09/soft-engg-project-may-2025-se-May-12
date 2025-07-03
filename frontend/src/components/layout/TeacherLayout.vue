<template>
  <div class="flex flex-col h-screen bg-gray-100 font-sans">
    <!-- Header -->
    <header class="flex justify-between items-center p-4 bg-white border-b shadow-sm">
      <div class="flex items-center">
        <h1 class="text-2xl font-bold text-gray-800 mr-8">GrowthGeine</h1>
        <nav class="hidden md:flex items-center space-x-2">
          <router-link v-for="item in navItems" :key="item.name" :to="item.path"
            class="px-4 py-2 rounded-md text-sm font-medium text-gray-600 hover:bg-gray-100 hover:text-gray-800 transition-colors duration-200"
            active-class="bg-blue-50 text-blue-600 font-semibold">
            {{ item.name }}
          </router-link>
        </nav>
      </div>
      <div class="flex items-center space-x-4">
        <button class="text-gray-500 hover:text-gray-700">
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6 6 0 10-12 0v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
        </button>
        <div class="relative">
          <button @click="toggleProfileMenu" class="flex items-center space-x-2">
            <img class="h-9 w-9 rounded-full object-cover" src="https://randomuser.me/api/portraits/women/68.jpg" alt="Teacher profile picture">
            <span class="hidden md:inline">Mrs. Johnson</span>
          </button>
          <div v-if="isProfileMenuOpen" class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-20">
            <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Profile</a>
            <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Settings</a>
            <a href="#" @click="logout" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Logout</a>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Content Area -->
      <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100 p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'TeacherLayout',
  setup() {
    const isProfileMenuOpen = ref(false)

    const navItems = [
      { name: 'Dashboard', path: '/teacher' },
      { name: 'My Students', path: '/teacher/students' },
      { name: 'Tasks', path: '/teacher/tasks' },
      { name: 'Reports', path: '/teacher/reports' },
    ]

    const toggleProfileMenu = () => {
      isProfileMenuOpen.value = !isProfileMenuOpen.value
    }

    const logout = () => {
      // Implement logout logic
      console.log('Logout action')
    }

    return { 
      navItems, 
      isProfileMenuOpen,
      toggleProfileMenu,
      logout
    }
  }
}
</script>

<style lang="postcss" scoped>
  .router-link-exact-active {
    @apply bg-blue-50 text-blue-600 font-semibold;
  }
</style>
