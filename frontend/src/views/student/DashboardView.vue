<template>
    <div class="min-h-screen bg-gray-50">
        <StudentNavBar />
        <div class="max-w-7xl mx-auto px-4 py-8">
            <!-- Header -->
            <div class="mb-8 flex flex-col md:flex-row md:items-center md:justify-between">
                <div>
                    <h1 class="text-3xl font-bold text-gray-900 mb-1">Welcome back, {{ userName }}!</h1>
                    <p class="text-lg text-gray-600">Here's your student dashboard overview.</p>
                </div>
            </div>
            <!-- Key Metrics -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
                <div class="bg-white rounded-xl shadow p-6 flex flex-col items-center">
                    <span class="text-3xl mb-2">🗒️</span>
                    <div class="font-bold text-lg text-gray-800">Tasks</div>
                    <div class="text-sm text-gray-500">Stay organized</div>
                    <router-link to="/student/tasks" class="mt-3 text-blue-600 hover:underline text-xs">View
                        Tasks</router-link>
                </div>
                <div class="bg-white rounded-xl shadow p-6 flex flex-col items-center">
                    <span class="text-3xl mb-2">💰</span>
                    <div class="font-bold text-lg text-gray-800">Finance</div>
                    <div class="text-sm text-gray-500">Track expenses</div>
                    <router-link to="/student/finance" class="mt-3 text-blue-600 hover:underline text-xs">View
                        Finance</router-link>
                </div>
                <div class="bg-white rounded-xl shadow p-6 flex flex-col items-center">
                    <span class="text-3xl mb-2">😊</span>
                    <div class="font-bold text-lg text-gray-800">Emotions</div>
                    <div class="text-sm text-gray-500">Mood & support</div>
                    <router-link to="/student/emotion" class="mt-3 text-blue-600 hover:underline text-xs">Emotion
                        Center</router-link>
                </div>
                <div class="bg-white rounded-xl shadow p-6 flex flex-col items-center">
                    <span class="text-3xl mb-2">🥗</span>
                    <div class="font-bold text-lg text-gray-800">Health</div>
                    <div class="text-sm text-gray-500">Meals & water</div>
                    <router-link to="/student/health" class="mt-3 text-blue-600 hover:underline text-xs">Health
                        Dashboard</router-link>
                </div>
                <div class="bg-white rounded-xl shadow p-6 flex flex-col items-center">
                    <span class="text-3xl mb-2">🔗</span>
                    <div class="font-bold text-lg text-gray-800">Connections</div>
                    <div class="text-sm text-gray-500">Teachers & Parents</div>
                    <router-link to="/student/my-connections" class="mt-3 text-blue-600 hover:underline text-xs">Manage
                        Connections</router-link>
                </div>
            </div>

            <div class="text-xs text-gray-400 text-center mt-8">Student Dashboard &mdash; All-in-one overview</div>
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