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
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
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
            </div>
            <!-- Health Analytics Card -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <!-- <div class="lg:col-span-2">
                     <div
                        class="bg-white rounded-xl shadow p-6 flex flex-col md:flex-row items-center md:items-start md:space-x-6 mb-8">
                        <span class="text-3xl mb-4 md:mb-0">📊</span>
                        <div>
                            <div class="font-bold text-lg text-gray-800 mb-1">Health Analytics</div>
                            <div class="text-sm text-gray-500 mb-2">See your health stats, trends, and AI tips.</div>
                            <router-link to="/student/health" class="text-blue-600 hover:underline text-xs">View Health
                                Analytics</router-link>
                        </div>
                    </div> 
            </div>-->
                <div>
                    <div class="bg-blue-50 border-l-4 border-blue-400 rounded-xl p-4 mb-4">
                        <div class="font-semibold text-blue-700 mb-1">Tip of the Day</div>
                        <div class="text-xs text-blue-900">Stay hydrated and take regular breaks while studying!</div>
                    </div>
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