<template>
  <div class="flex min-h-screen flex-col bg-gray-100 font-sans">
    <header class="sticky top-0 z-30 bg-white shadow-sm border-b">
      <div class="mx-auto max-w-7xl flex items-center justify-between px-4 py-3">
        <div class="flex items-center gap-6">
          <RouterLink to="/teacher" class="text-xl font-bold text-blue-700">
            GrowthGenie
          </RouterLink>

          <nav class="hidden md:flex items-center gap-3">
            <RouterLink v-for="item in navItems" :key="item.name" :to="item.path"
              class="rounded-md px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 transition"
              exact-active-class="bg-blue-50 text-blue-600 font-semibold">
              {{ item.name }}
            </RouterLink>
          </nav>
        </div>

        <div class="flex items-center gap-3">
          <div class="relative" ref="profileMenuContainer">
            <button @click="toggleProfileMenu"
              class="flex items-center gap-2 px-2 py-1 rounded-md hover:bg-gray-100" aria-haspopup="true"
              :aria-expanded="isProfileMenuOpen">
              <span class="hidden md:inline text-sm text-gray-700">{{ displayName }}</span>
              <svg class="h-5 w-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <div v-if="isProfileMenuOpen"
              class="absolute right-0 mt-2 w-48 rounded-md bg-white shadow-lg ring-1 ring-black/10">
              <RouterLink to="/teacher" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" @click="isProfileMenuOpen = false">
                Profile
              </RouterLink>
              <RouterLink to="/teacher/settings" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" @click="isProfileMenuOpen = false">
                Settings
              </RouterLink>
              <button class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50" @click="logout">
                Logout
              </button>
            </div>
          </div>

          <button class="md:hidden p-2 text-gray-600 hover:bg-gray-100 rounded" @click="mobileOpen = !mobileOpen">
            <svg v-if="!mobileOpen" class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg v-else class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <nav v-if="mobileOpen" class="md:hidden border-t bg-white">
        <div class="px-4 py-2">
          <RouterLink v-for="item in navItems" :key="item.name" :to="item.path"
            class="block rounded-md px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
            exact-active-class="bg-blue-50 text-blue-600 font-semibold" @click="mobileOpen = false">
            {{ item.name }}
          </RouterLink>
        </div>
      </nav>
    </header>

    <main class="flex-1 overflow-y-auto px-4 py-6">
      <div class="mx-auto max-w-7xl">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const navItems = [
  { name: 'Dashboard', path: '/teacher' },
  { name: 'My Students', path: '/teacher/students' },
  { name: 'Tasks', path: '/teacher/tasks' },
  { name: 'Reports', path: '/teacher/reports' },
]

const isProfileMenuOpen = ref(false)
const mobileOpen = ref(false)
const profileMenuContainer = ref(null)

const displayNameManual = ref('')
const token = computed(() => store.getters['auth/token'] || store.state.auth?.token || '')

const displayName = computed(() =>
  displayNameManual.value ||
  store.getters['auth/user']?.full_name ||
  store.state.auth?.user?.full_name ||
  (store.state.auth?.user?.email ? store.state.auth.user.email.split('@')[0] : '') ||
  'Teacher'
)

const toggleProfileMenu = () => {
  isProfileMenuOpen.value = !isProfileMenuOpen.value
}

const onDocClick = (e) => {
  if (profileMenuContainer.value && !profileMenuContainer.value.contains(e.target)) {
    isProfileMenuOpen.value = false
  }
}

const logout = async () => {
  try {
    await store.dispatch('auth/logout')
  } catch {}
  isProfileMenuOpen.value = false
  mobileOpen.value = false
  router.push('/login/teacher')
}

onMounted(async () => {
  document.addEventListener('click', onDocClick)

  if (!store.getters['auth/user']?.full_name && token.value) {
    try {
      const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
      const { data } = await axios.get(`${API_BASE}/users/me`, {
        headers: { Authorization: `Bearer ${token.value}` },
      })
      displayNameManual.value = data?.full_name || data?.email?.split('@')[0] || ''
    } catch {}
  }
})

onBeforeUnmount(() => {
  document.removeEventListener('click', onDocClick)
})
</script>
