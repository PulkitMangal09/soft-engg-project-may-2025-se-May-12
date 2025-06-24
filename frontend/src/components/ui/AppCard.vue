<template>
    <div :class="cardClasses">
        <div v-if="hasHeader" class="card-header px-6 py-4 border-b border-gray-200">
            <div class="flex items-center justify-between">
                <div class="flex items-center">
                    <span v-if="icon" class="text-2xl mr-3">{{ icon }}</span>
                    <div>
                        <h3 v-if="title" class="text-lg font-semibold text-gray-900">{{ title }}</h3>
                        <p v-if="subtitle" class="text-sm text-gray-600">{{ subtitle }}</p>
                    </div>
                </div>
                <div v-if="$slots.action" class="flex items-center">
                    <slot name="action"></slot>
                </div>
            </div>
        </div>

        <div :class="contentClasses">
            <slot></slot>
        </div>

        <div v-if="$slots.footer" class="card-footer px-6 py-4 border-t border-gray-200">
            <slot name="footer"></slot>
        </div>
    </div>
</template>

<script>
export default {
    name: 'AppCard',
    props: {
        title: String,
        subtitle: String,
        icon: String,
        variant: {
            type: String,
            default: 'default', // default, success, warning, error
            validator: value => ['default', 'success', 'warning', 'error'].includes(value)
        },
        padding: {
            type: String,
            default: 'normal', // none, sm, normal, lg
            validator: value => ['none', 'sm', 'normal', 'lg'].includes(value)
        }
    },

    computed: {
        hasHeader() {
            return this.title || this.subtitle || this.icon || this.$slots.action
        },

        cardClasses() {
            const base = 'bg-white rounded-xl shadow-sm border'

            const variants = {
                default: 'border-gray-200',
                success: 'border-l-4 border-l-green-500 border-gray-200',
                warning: 'border-l-4 border-l-yellow-500 border-gray-200',
                error: 'border-l-4 border-l-red-500 border-gray-200'
            }

            return [base, variants[this.variant]].join(' ')
        },

        contentClasses() {
            const paddings = {
                none: '',
                sm: 'p-3',
                normal: 'p-6',
                lg: 'p-8'
            }

            const basePadding = this.hasHeader ? '' : paddings[this.padding]
            const topPadding = this.hasHeader ? 'pt-0' : ''

            return [basePadding, topPadding].filter(Boolean).join(' ')
        }
    }
}
</script>