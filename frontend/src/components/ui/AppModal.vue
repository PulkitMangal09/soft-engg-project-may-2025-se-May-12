<template>
    <teleport to="body">
        <transition name="modal">
            <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto">
                <div class="flex min-h-screen items-center justify-center p-4">
                    <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity" @click="closeModal"></div>

                    <div :class="modalClasses">
                        <!-- Header -->
                        <div v-if="title || $slots.header"
                            class="flex items-center justify-between p-6 border-b border-gray-200">
                            <div v-if="$slots.header">
                                <slot name="header"></slot>
                            </div>
                            <div v-else>
                                <h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
                                <p v-if="subtitle" class="text-sm text-gray-600">{{ subtitle }}</p>
                            </div>

                            <button @click="closeModal" class="text-gray-400 hover:text-gray-600 transition-colors">
                                ✕
                            </button>
                        </div>

                        <!-- Body -->
                        <div :class="bodyClasses">
                            <slot></slot>
                        </div>

                        <!-- Footer -->
                        <div v-if="$slots.footer" class="flex justify-end space-x-3 p-6 border-t border-gray-200">
                            <slot name="footer"></slot>
                        </div>
                    </div>
                </div>
            </div>
        </transition>
    </teleport>
</template>

<script>
export default {
    name: 'AppModal',
    emits: ['close'],
    props: {
        show: {
            type: Boolean,
            default: false
        },
        title: String,
        subtitle: String,
        size: {
            type: String,
            default: 'md', // sm, md, lg, xl
            validator: value => ['sm', 'md', 'lg', 'xl'].includes(value)
        },
        closeOnBackdrop: {
            type: Boolean,
            default: true
        }
    },

    computed: {
        modalClasses() {
            const base = 'relative bg-white rounded-lg shadow-xl transform transition-all'

            const sizes = {
                sm: 'max-w-sm w-full',
                md: 'max-w-md w-full',
                lg: 'max-w-lg w-full',
                xl: 'max-w-xl w-full'
            }

            return [base, sizes[this.size]].join(' ')
        },

        bodyClasses() {
            const base = 'p-6'
            const noPadding = this.$slots.header || this.$slots.footer ? '' : base

            return noPadding || base
        }
    },

    methods: {
        closeModal() {
            if (this.closeOnBackdrop) {
                this.$emit('close')
            }
        }
    },

    watch: {
        show(newVal) {
            if (newVal) {
                document.body.style.overflow = 'hidden'
            } else {
                document.body.style.overflow = ''
            }
        }
    },

    beforeUnmount() {
        document.body.style.overflow = ''
    }
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
    transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
    opacity: 0;
}
</style>