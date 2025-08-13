<template>
  <div class="min-h-screen bg-gray-100">
    <StudentNavBar />
    <div class="max-w-7xl mx-auto px-4 py-8">
      
      <header class="bg-white rounded-2xl shadow-lg p-6 md:p-10 mb-8 flex flex-col md:flex-row items-center justify-between">
        <div class="text-center md:text-left">
          <h1 class="text-3xl md:text-4xl font-extrabold text-gray-900 mb-2 leading-tight">Welcome back, {{ userName }}! 👋</h1>
          <p class="text-base md:text-lg text-gray-500">Here's your student dashboard overview. Stay on top of your well-being and tasks.</p>
        </div>
        <div class="hidden md:block text-6xl text-gray-300 ml-8">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-20 w-20" viewBox="0 0 20 20" fill="currentColor">
            <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 110-6 3 3 0 010 6z" />
          </svg>
        </div>
      </header>

      <section>
        <h2 class="text-2xl font-bold text-gray-800 mb-4">Your Tools</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
          <router-link to="/student/tasks" class="dashboard-card group">
            <span class="text-4xl mb-3 transition-transform group-hover:scale-110">🗒️</span>
            <div class="font-bold text-lg text-gray-800">Tasks</div>
            <div class="text-sm text-gray-500 mt-1">Manage your to-do list</div>
          </router-link>
          
          <router-link to="/student/finance" class="dashboard-card group">
            <span class="text-4xl mb-3 transition-transform group-hover:scale-110">💰</span>
            <div class="font-bold text-lg text-gray-800">Finance</div>
            <div class="text-sm text-gray-500 mt-1">Track your spending</div>
          </router-link>
          
          <router-link to="/student/emotion" class="dashboard-card group">
            <span class="text-4xl mb-3 transition-transform group-hover:scale-110">😊</span>
            <div class="font-bold text-lg text-gray-800">Emotions</div>
            <div class="text-sm text-gray-500 mt-1">Log your mood & get support</div>
          </router-link>
          
          <router-link to="/student/health" class="dashboard-card group">
            <span class="text-4xl mb-3 transition-transform group-hover:scale-110">🥗</span>
            <div class="font-bold text-lg text-gray-800">Health</div>
            <div class="text-sm text-gray-500 mt-1">Monitor vitals & diet</div>
          </router-link>
          
          <router-link to="/student/my-connections" class="dashboard-card group">
            <span class="text-4xl mb-3 transition-transform group-hover:scale-110">🔗</span>
            <div class="font-bold text-lg text-gray-800">Connections</div>
            <div class="text-sm text-gray-500 mt-1">Manage teachers & parents</div>
          </router-link>
        </div>
      </section>

      <div class="text-xs text-gray-400 text-center mt-12">
        Student Dashboard &mdash; Your all-in-one overview
      </div>
    </div>
  </div>
</template>

<script>
import StudentNavBar from '@/components/layout/StudentNavBar.vue'
import { mapGetters } from 'vuex'
export default {
    name: 'StudentDashboard',
    components: { StudentNavBar },
    computed: {
        ...mapGetters('auth', ['currentUser']),
        userName() {
            return this.currentUser?.name || 'Student'
        }
    }
}
</script>

<style scoped>
.dashboard-card {
  @apply flex flex-col items-center bg-white rounded-xl shadow-md p-6 
         text-center transition-all duration-300 ease-in-out cursor-pointer;
}

.dashboard-card:hover {
  @apply transform scale-105 shadow-xl;
}
</style>