<template>
  <nav class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-30">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Left: Logo and Title -->
        <router-link to="/student" class="flex items-center space-x-2">
          <span class="text-2xl">🎓</span>
          <span class="font-bold text-lg text-gray-900 hidden sm:inline">Student Portal</span>
        </router-link>
        <!-- Center: Navigation Links (desktop) -->
        <div class="hidden md:flex space-x-6">
          <router-link v-for="item in navItems" :key="item.to" :to="item.to"
            class="flex items-center px-2 py-1 rounded-lg text-gray-600 hover:text-blue-600 hover:bg-blue-50 transition"
            :class="{ 'bg-blue-100 text-blue-700 font-semibold': $route.path.startsWith(item.to) }">
            <span class="text-xl mr-1">{{ item.icon }}</span>
            <span class="text-sm">{{ item.label }}</span>
          </router-link>
        </div>
        <!-- Right: Profile Dropdown -->
        <div class="relative">
          <button @click="showProfileMenu = !showProfileMenu"
            class="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100">
            <div class="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
              🎓
            </div>
            <span class="text-sm font-medium text-gray-700">{{ userName }}</span>
          </button>
          <!-- Profile dropdown -->
          <div v-if="showProfileMenu"
            class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-200 z-10">
            <div class="py-1">
              <router-link to="/student/profile"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Profile</router-link>
              <router-link to="/student/settings"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Settings</router-link>
              <hr class="my-1">
              <button @click="logout"
                class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Sign out</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Bottom nav for mobile -->
    <div
      class="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 flex justify-around py-2 px-4 z-40">
      <router-link v-for="item in navItems" :key="item.to" :to="item.to"
        class="flex flex-col items-center py-1 px-2 rounded-lg transition-colors"
        :class="{ 'text-blue-600 bg-blue-50': $route.path.startsWith(item.to), 'text-gray-500 hover:text-blue-500': !$route.path.startsWith(item.to) }">
        <span class="text-2xl">{{ item.icon }}</span>
        <span class="text-xs mt-0.5">{{ item.label }}</span>
      </router-link>
    </div>
  </nav>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'StudentNavBar',
  data() {
    return {
      showProfileMenu: false,
      navItems: [
        { label: 'Dashboard', icon: '🏠', to: '/student' },
        { label: 'Tasks', icon: '🗒️', to: '/student/tasks' },
        { label: 'Finance', icon: '💰', to: '/student/finance' },
        { label: 'Emotions', icon: '😊', to: '/student/emotion' },
        { label: 'Health', icon: '🥗', to: '/student/health' },
        // { label: 'Health', icon: '📊', to: '/student/health' },
      ]
    }
  },
  computed: {
    ...mapGetters('auth', ['currentUser']),
    userName() {
      return this.currentUser?.name || 'Student'
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('auth/logout')
      this.$router.push('/')
    }
  },
  mounted() {
    document.addEventListener('click', (e) => {
      if (!this.$el.contains(e.target)) {
        this.showProfileMenu = false
      }
    })
  }
}
</script>