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

            <form @submit.prevent="handleSignup" class="space-y-6">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
                    <input v-model="form.name" type="text" required
                        class="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Enter your full name">
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
                    <input v-model="form.email" type="email" required
                        class="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Enter your email">
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Password</label>
                    <input v-model="form.password" type="password" required
                        class="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Create a password">
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Confirm Password</label>
                    <input v-model="form.confirmPassword" type="password" required
                        class="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Confirm your password">
                </div>

                <div class="flex items-start">
                    <input v-model="form.acceptTerms" type="checkbox" required class="mt-1 mr-3">
                    <label class="text-sm text-gray-600">
                        I agree to the <a href="#" class="text-blue-500 hover:underline">Terms of Service</a>
                        and <a href="#" class="text-blue-500 hover:underline">Privacy Policy</a>
                    </label>
                </div>

                <button type="submit" :disabled="loading"
                    class="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold py-3 px-6 rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50">
                    <span v-if="loading">Creating account...</span>
                    <span v-else>Create Account</span>
                </button>
            </form>

            <div class="mt-6 text-center">
                <p class="text-sm text-gray-600">
                    Already have an account?
                    <router-link :to="`/login/${role}`" class="text-blue-500 hover:underline">Sign In</router-link>
                </p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'SignupView',
    props: {
        role: {
            type: String,
            default: 'student'
        }
    },

    data() {
        return {
            form: {
                name: '',
                email: '',
                password: '',
                confirmPassword: '',
                acceptTerms: false
            },
            loading: false
        }
    },

    computed: {
        roleConfig() {
            const configs = {
                student: {
                    title: 'Create Student Account',
                    subtitle: 'Join thousands of students improving their lives',
                    icon: '👨‍🎓',
                    bgClass: 'bg-gradient-to-br from-blue-500 to-blue-600'
                },
                teacher: {
                    title: 'Teacher Registration',
                    subtitle: 'Join our educator community',
                    icon: '👨‍🏫',
                    bgClass: 'bg-gradient-to-br from-orange-500 to-orange-600'
                },
                parent: {
                    title: 'Create Parent Account',
                    subtitle: 'Monitor and support your child\'s journey',
                    icon: '👨‍👩‍👧‍👦',
                    bgClass: 'bg-gradient-to-br from-purple-500 to-purple-600'
                }
            }
            return configs[this.role] || configs.student
        }
    },

    methods: {
        async handleSignup() {
            if (this.form.password !== this.form.confirmPassword) {
                alert('Passwords do not match')
                return
            }

            this.loading = true
            try {
                // Handle signup logic here
                console.log('Signup attempt:', this.form, this.role)
                // Simulate API call
                setTimeout(() => {
                    this.loading = false
                    alert('Account created successfully!')
                    this.$router.push(`/login/${this.role}`)
                }, 1000)
            } catch (error) {
                console.error('Signup error:', error)
                this.loading = false
            }
        }
    }
}
</script>