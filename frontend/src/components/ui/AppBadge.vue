<template>
    <span :class="badgeClasses">
        <span v-if="icon" class="mr-1">{{ icon }}</span>
        <slot></slot>
    </span>
</template>

<script>
export default {
    name: 'AppBadge',
    props: {
        variant: {
            type: String,
            default: 'default', // default, success, warning, error, info
            validator: value => ['default', 'success', 'warning', 'error', 'info'].includes(value)
        },
        size: {
            type: String,
            default: 'md', // sm, md, lg
            validator: value => ['sm', 'md', 'lg'].includes(value)
        },
        icon: String,
        rounded: {
            type: Boolean,
            default: false
        }
    },

    computed: {
        badgeClasses() {
            const base = 'inline-flex items-center font-medium'

            const sizes = {
                sm: 'px-2 py-1 text-xs',
                md: 'px-2.5 py-1.5 text-sm',
                lg: 'px-3 py-2 text-base'
            }

            const variants = {
                default: 'bg-gray-100 text-gray-800',
                success: 'bg-green-100 text-green-800',
                warning: 'bg-yellow-100 text-yellow-800',
                error: 'bg-red-100 text-red-800',
                info: 'bg-blue-100 text-blue-800'
            }

            const rounded = this.rounded ? 'rounded-full' : 'rounded-md'

            return [base, sizes[this.size], variants[this.variant], rounded].join(' ')
        }
    }
}
</script>