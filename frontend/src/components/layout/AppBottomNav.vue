<template>
    <nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-40">
        <div class="flex justify-around items-center h-16 px-4">
            <router-link v-for="item in navItems" :key="item.name" :to="item.to" :class="navItemClasses(item)"
                class="flex flex-col items-center justify-center min-w-0 flex-1 py-2">
                <span class="text-xl mb-1">{{ item.icon }}</span>
                <span class="text-xs font-medium truncate">{{ item.label }}</span>
            </router-link>
        </div>
    </nav>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
    name: 'AppBottomNav',
    computed: {
        ...mapGetters('auth', ['userRole']),

        navItems() {
            const items = {
                student: [
                    { name: 'dashboard', label: 'Dashboard', icon: '🏠', to: '/student' },
                    { name: 'tasks', label: 'Tasks', icon: '📝', to: '/student/tasks' },
                    { name: 'finance', label: 'Finance', icon: '💰', to: '/student/finance' },
                    { name: 'emotion', label: 'Emotion', icon: '😊', to: '/student/emotion' },
                    { name: 'health', label: 'Health', icon: '🍎', to: '/student/health' }
                ],
                teacher: [
                    { name: 'dashboard', label: 'Dashboard', icon: '🏠', to: '/teacher' },
                    { name: 'students', label: 'Students', icon: '👥', to: '/teacher/students' },
                    { name: 'tasks', label: 'Tasks', icon: '📝', to: '/teacher/tasks' },
                    { name: 'reports', label: 'Reports', icon: '📊', to: '/teacher/reports' }
                ],
                parent: [
                    { name: 'dashboard', label: 'Dashboard', icon: '🏠', to: '/parent' },
                    { name: 'analytics', label: 'Analytics', icon: '📊', to: '/parent/analytics' },
                    { name: 'tasks', label: 'Tasks', icon: '📝', to: '/parent/tasks' },
                    { name: 'family', label: 'Family', icon: '👨‍👩‍👧‍👦', to: '/parent/family' }
                ]
            }

            return items[this.userRole] || items.student
        }
    },

    methods: {
        navItemClasses(item) {
            const isActive = this.$route.path === item.to
            return isActive
                ? `text-${this.userRole}-500`
                : 'text-gray-400 hover:text-gray-600'
        }
    }
}
</script>