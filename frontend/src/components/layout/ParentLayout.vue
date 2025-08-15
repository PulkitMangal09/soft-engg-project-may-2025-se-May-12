<template>
  <div class="flex min-h-screen flex-col bg-gray-100 font-sans">
    <!-- Header -->
    <header class="sticky top-0 z-30 border-b bg-white shadow-sm">
      <div class="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
        <!-- Left: brand + desktop nav -->
        <div class="flex items-center gap-6">
          <RouterLink to="/parent/dashboard" class="text-2xl font-bold text-gray-800">
            GrowthGeine
          </RouterLink>

          <!-- Desktop nav -->
          <nav class="hidden md:flex items-center gap-1">
            <RouterLink v-for="item in navItems" :key="item.name" :to="item.path"
              class="rounded-md px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 hover:text-gray-800 transition-colors"
              exact-active-class="bg-blue-50 text-blue-600 font-semibold">
              {{ item.name }}
            </RouterLink>
          </nav>
        </div>

        <!-- Right: profile -->
        <div class="flex items-center gap-3">
          <div class="relative">
            <button @click="toggleProfileMenu" class="flex items-center gap-2 rounded-md px-2 py-1 hover:bg-gray-100"
              aria-haspopup="menu" :aria-expanded="isProfileMenuOpen">
              <span class="hidden md:inline text-sm text-gray-700">{{ displayName }}</span>
              <svg class="h-4 w-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>

            <div v-if="isProfileMenuOpen"
              class="absolute right-0 mt-2 w-48 rounded-md bg-white py-1 shadow-lg ring-1 ring-black/5" role="menu">
              <RouterLink to="/parent/dashboard" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" role="menuitem"
                @click="isProfileMenuOpen = false">
                Profile
              </RouterLink>
              <RouterLink to="/parent/settings" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" role="menuitem"
                @click="isProfileMenuOpen = false">
                Settings
              </RouterLink>
              <button class="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100" role="menuitem"
                @click="logout">
                Logout
              </button>
            </div>
          </div>

          <!-- Mobile menu button -->
          <button class="md:hidden rounded-md p-2 text-gray-600 hover:bg-gray-100" @click="mobileOpen = !mobileOpen"
            aria-label="Toggle menu">
            <svg v-if="!mobileOpen" class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg v-else class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile nav -->
      <nav v-if="mobileOpen" class="md:hidden border-t bg-white">
        <div class="mx-auto flex max-w-7xl flex-col px-4 py-2">
          <RouterLink v-for="item in navItems" :key="item.name" :to="item.path"
            class="rounded-md px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
            exact-active-class="bg-blue-50 text-blue-600 font-semibold" @click="mobileOpen = false">
            {{ item.name }}
          </RouterLink>
        </div>
      </nav>
    </header>

    <!-- Main content (single router-view only) -->
    <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100">
      <div class="mx-auto max-w-7xl px-4 py-6">
        <router-view />
      </div>
    </main>
  </div>
  
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const navItems = [
  { name: 'Dashboard', path: '/parent/dashboard' },
  { name: 'Analytics', path: '/parent/analytics' },
  { name: 'Reports', path: '/parent/reports' },
]

const isProfileMenuOpen = ref(false)
const mobileOpen = ref(false)

const token = computed(() => store.getters['auth/token'] || store.state.auth?.token || '')
const displayNameManual = ref('')
const displayName = computed(() =>
  displayNameManual.value ||
  store.getters['auth/user']?.full_name ||
  store.state.auth?.user?.full_name ||
  (store.state.auth?.user?.email ? store.state.auth.user.email.split('@')[0] : '') ||
  'Parent'
)
const toggleProfileMenu = () => { isProfileMenuOpen.value = !isProfileMenuOpen.value }

const onDocClick = (e) => {
  const menu = document.querySelector('[role="menu"]')
  const btn = e.target.closest('button')
  if (!menu) return
  if (!menu.contains(e.target) && !btn) isProfileMenuOpen.value = false
}
onMounted(() => {
  document.addEventListener('click', onDocClick)
})
onBeforeUnmount(() => document.removeEventListener('click', onDocClick))

const logout = async () => {
  try { await store.dispatch('auth/logout') } catch { }
  isProfileMenuOpen.value = false
  mobileOpen.value = false
  router.push('/')
}
</script>

<style scoped>
/* Active link styling handled via exact-active-class attributes */
</style>
