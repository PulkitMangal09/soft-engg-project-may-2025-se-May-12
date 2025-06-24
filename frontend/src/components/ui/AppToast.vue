<template>
    <transition-group name="toast" tag="div" class="fixed top-4 right-4 z-50 space-y-2">
        <div v-for="toast in toasts" :key="toast.id" :class="toastClasses(toast.type)">
            <div class="flex items-start">
                <div class="flex-shrink-0">
                    <span class="text-xl">{{ getIcon(toast.type) }}</span>
                </div>
                <div class="ml-3 flex-1">
                    <p class="text-sm font-medium">{{ toast.title }}</p>
                    <p v-if="toast.message" class="text-sm opacity-90">{{ toast.message }}</p>
                </div>
                <button @click="removeToast(toast.id)" class="ml-4 flex-shrink-0 text-white/70 hover:text-white">
                    ✕
                </button>
            </div>
        </div>
    </transition-group>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: 'AppToast',
    computed: {
        ...mapState('ui', ['toasts'])
    },

    methods: {
        removeToast(id) {
            this.$store.commit('ui/REMOVE_TOAST', id)
        },

        toastClasses(type) {
            const base = 'max-w-sm w-full bg-white shadow-lg rounded-lg pointer-events-auto border-l-4 p-4'

            const types = {
                success: 'border-green-500 bg-green-50',
                error: 'border-red-500 bg-red-50',
                warning: 'border-yellow-500 bg-yellow-50',
                info: 'border-blue-500 bg-blue-50'
            }

            return [base, types[type] || types.info].join(' ')
        },

        getIcon(type) {
            const icons = {
                success: '✅',
                error: '❌',
                warning: '⚠️',
                info: 'ℹ️'
            }

            return icons[type] || icons.info
        }
    }
}
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
    transition: all 0.3s ease;
}

.toast-enter-from {
    opacity: 0;
    transform: translateX(100%);
}

.toast-leave-to {
    opacity: 0;
    transform: translateX(100%);
}
</style>