<template>
    <header class="bg-white shadow-sm border-b border-gray-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <!-- Left side -->
                <div class="flex items-center">
                    <button v-if="showMenuButton" @click="toggleSidebar"
                        class="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100">
                        ☰
                    </button>

                    <div class="flex items-center ml-4">
                        <div
                            class="app-logo w-8 h-8 rounded-lg gradient-primary flex items-center justify-center text-white text-lg font-bold mr-3">
                            {{ roleIcon }}
                        </div>
                        <div>
                            <h1 class="text-lg font-semibold text-gray-900">{{ title }}</h1>
                            <p v-if="subtitle" class="text-sm text-gray-500">{{ subtitle }}</p>
                        </div>
                    </div>
                </div>

                <!-- Right side -->
                <div class="flex items-center space-x-4">
                    <button v-if="showNotifications"
                        class="p-2 rounded-full text-gray-400 hover:text-gray-500 hover:bg-gray-100 relative">
                        🔔
                        <span v-if="notificationCount > 0"
                            class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                            {{ notificationCount }}
                        </span>
                    </button>

                    <div class="relative">
                        <button @click="showProfileMenu = !showProfileMenu"
                            class="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100">
                            <div class="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
                                {{ userRole === 'student' ? '👨‍🎓' : userRole === 'teacher' ? '👨‍🏫' : '👨‍👩‍👧‍👦'
                                }}
                            </div>
                            <span class="text-sm font-medium text-gray-700">{{ userName }}</span>
                        </button>

                        <!-- Profile dropdown -->
                        <div v-if="showProfileMenu"
                            class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-200 z-10">
                            <div class="py-1">
                                <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Profile</a>
                                <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Settings</a>
                                <hr class="my-1">
                                <button @click="logout"
                                    class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                    Sign out
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </header>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
    name: 'AppHeader',
    props: {
        title: {
            type: String,
            required: true
        },
        subtitle: String,
        showMenuButton: {
            type: Boolean,
            default: true
        },
        showNotifications: {
            type: Boolean,
            default: true
        },
        notificationCount: {
            type: Number,
            default: 0
        }
    },

    data() {
        return {
            showProfileMenu: false
        }
    },

    computed: {
        ...mapGetters('auth', ['userRole', 'currentUser']),

        userName() {
            return this.currentUser?.name || 'User'
        },

        roleIcon() {
            const icons = {
                student: '🎓',
                teacher: '🏫',
                parent: '👨‍👩‍👧‍👦'
            }
            return icons[this.userRole] || '🎓'
        }
    },

    methods: {
        toggleSidebar() {
            this.$store.commit('ui/TOGGLE_SIDEBAR')
        },

        logout() {
            this.$store.dispatch('auth/logout')
            this.$router.push('/')
        }
    },

    mounted() {
        // Close profile menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.$el.contains(e.target)) {
                this.showProfileMenu = false
            }
        })
    }
}
</script>