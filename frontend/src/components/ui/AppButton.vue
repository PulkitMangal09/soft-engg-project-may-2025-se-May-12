<template>
  <button
    :class="buttonClasses"
    :disabled="disabled"
    @click="$emit('click')"
  >
    <span v-if="icon" class="mr-2">{{ icon }}</span>
    <span v-if="label">{{ label }}</span>
    <slot v-else></slot>
  </button>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'AppButton',
  emits: ['click'],
  props: {
    label: String,
    variant: {
      type: String,
      default: 'primary', // primary, secondary, success, error, warning
      validator: (value) => ['primary', 'secondary', 'success', 'error', 'warning'].includes(value),
    },
    size: {
      type: String,
      default: 'md', // sm, md, lg
      validator: (value) => ['sm', 'md', 'lg'].includes(value),
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    icon: String,
  },
  setup(props) {
    const buttonClasses = computed(() => {
      const base = 'inline-flex items-center justify-center font-semibold rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors'
      
      const variants = {
        primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
        secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300 focus:ring-gray-400',
        success: 'bg-green-600 text-white hover:bg-green-700 focus:ring-green-500',
        error: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
        warning: 'bg-yellow-500 text-white hover:bg-yellow-600 focus:ring-yellow-400',
      }

      const sizes = {
        sm: 'px-3 py-1.5 text-sm',
        md: 'px-4 py-2 text-base',
        lg: 'px-6 py-3 text-lg',
      }

      const disabledClasses = props.disabled ? 'opacity-50 cursor-not-allowed' : ''

      return [base, variants[props.variant], sizes[props.size], disabledClasses].join(' ')
    })

    return {
      buttonClasses,
    }
  },
}
</script>