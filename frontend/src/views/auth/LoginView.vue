<template>
    <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div class="max-w-md w-full">
            <div class="text-center mb-8">
                <div
                    :class="['w-16 h-16 rounded-2xl flex items-center justify-center text-2xl text-white mx-auto mb-4', roleConfig.bgClass]">
                    {{ roleConfig.icon }}
                </div>
                <h1 class="text-2xl font-bold text-gray-900 mb-2">{{ roleConfig.title }}</h1>
                <p class="text-gray-600">{{ roleConfig.subtitle }}</p>
            </div>

            <!-- Development mode notice -->
            <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <svg class="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                        </svg>
                    </div>
                    <div class="ml-3">
                        <p class="text-sm text-yellow-800">
                            <strong>Development Mode:</strong> Authentication is bypassed. Click "Sign In" to proceed directly to the dashboard.
                        </p>
                    </div>
                </div>
            </div>

            <form @submit.prevent="handleLogin" class="space-y-6">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
                    <input v-model="form.email" type="email"
                        class="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Enter your email (optional)">
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Password</label>
                    <input v-model="form.password" type="password"
                        class="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Enter your password (optional)">
                </div>

                <button type="submit" :disabled="loading"
                    class="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold py-3 px-6 rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50">
                    <span v-if="loading">Signing in...</span>
                    <span v-else>Sign In (Dev Mode)</span>
                </button>
            </form>

            <div class="mt-6 text-center">
                <p class="text-sm text-gray-600">
                    Don't have an account?
                    <router-link :to="`/signup/${role}`" class="text-blue-500 hover:underline">Sign Up</router-link>
                </p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'LoginView',
    props: {
        role: {
            type: String,
            default: 'student'
        }
    },

    data() {
        return {
            form: {
                email: '',
                password: ''
            },
            loading: false
        }
    },

    computed: {
        roleConfig() {
            const configs = {
                student: {
                    title: 'Student Login',
                    subtitle: 'Welcome back! Let\'s continue learning',
                    icon: '👨‍🎓',
                    bgClass: 'bg-gradient-to-br from-blue-500 to-blue-600'
                },
                teacher: {
                    title: 'Teacher Login',
                    subtitle: 'Welcome back, educator!',
                    icon: '👨‍🏫',
                    bgClass: 'bg-gradient-to-br from-orange-500 to-orange-600'
                },
                parent: {
                    title: 'Parent Login',
                    subtitle: 'Stay connected with your child\'s progress',
                    icon: '👨‍👩‍👧‍👦',
                    bgClass: 'bg-gradient-to-br from-purple-500 to-purple-600'
                }
            }
            return configs[this.role] || configs.student
        }
    },

    methods: {
        async handleLogin() {
            this.loading = true
            try {
                // Bypass authentication for now - directly set user role and navigate
                await this.$store.dispatch('auth/loginWithoutValidation', {
                    role: this.role
                })
                
                // Navigate to the respective dashboard
                this.$router.push(`/${this.role}`)
            } catch (error) {
                console.error('Login error:', error)
                alert('An error occurred during login')
            } finally {
                this.loading = false
            }
        }
    }
}
</script>