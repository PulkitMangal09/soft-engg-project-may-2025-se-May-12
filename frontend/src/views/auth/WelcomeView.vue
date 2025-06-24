<template>
    <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div class="max-w-md w-full">
            <div class="text-center mb-8">
                <div
                    class="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center text-3xl text-white mx-auto mb-4">
                    🎓
                </div>
                <h1 class="text-3xl font-bold text-gray-900 mb-2">GrowthGeine</h1>
                <p class="text-gray-600">Student Life Management Platform</p>
            </div>

            <div class="space-y-4 mb-8">
                <div v-for="role in roles" :key="role.value" @click="selectedRole = role.value" :class="[
                    'p-4 border-2 rounded-xl cursor-pointer transition-all',
                    selectedRole === role.value
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                ]">
                    <div class="flex items-center">
                        <div
                            :class="['w-12 h-12 rounded-full flex items-center justify-center text-xl mr-4', role.bgClass]">
                            {{ role.icon }}
                        </div>
                        <div>
                            <h3 class="font-semibold text-gray-900">{{ role.name }}</h3>
                            <p class="text-sm text-gray-600">{{ role.description }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <button @click="getStarted"
                class="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold py-3 px-6 rounded-lg hover:opacity-90 transition-opacity mb-4">
                Get Started
            </button>

            <p class="text-center text-sm text-gray-600">
                Already have an account?
                <router-link to="/login" class="text-blue-500 hover:underline">Sign In</router-link>
            </p>
        </div>
    </div>
</template>

<script>
export default {
    name: 'WelcomeView',
    data() {
        return {
            selectedRole: 'student',
            roles: [
                {
                    value: 'student',
                    name: 'Student',
                    description: 'Manage tasks, finances, health, and emotions',
                    icon: '👨‍🎓',
                    bgClass: 'bg-blue-100 text-blue-600'
                },
                {
                    value: 'teacher',
                    name: 'Teacher',
                    description: 'Monitor classroom and student progress',
                    icon: '👨‍🏫',
                    bgClass: 'bg-orange-100 text-orange-600'
                },
                {
                    value: 'parent',
                    name: 'Parent',
                    description: 'Track children\'s activities and well-being',
                    icon: '👨‍👩‍👧‍👦',
                    bgClass: 'bg-purple-100 text-purple-600'
                }
            ]
        }
    },

    methods: {
        getStarted() {
            this.$router.push(`/signup/${this.selectedRole}`)
        }
    }
}
</script>