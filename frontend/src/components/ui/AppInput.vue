<template>
    <div class="form-group">
        <label v-if="label" :for="inputId" class="block text-sm font-medium text-gray-700 mb-2">
            {{ label }}
            <span v-if="required" class="text-red-500">*</span>
        </label>

        <div class="relative">
            <input :id="inputId" :type="type" :value="modelValue" :placeholder="placeholder" :required="required"
                :disabled="disabled" :class="inputClasses" @input="$emit('update:modelValue', $event.target.value)"
                @focus="$emit('focus')" @blur="$emit('blur')">

            <div v-if="icon" class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <span class="text-gray-400">{{ icon }}</span>
            </div>
        </div>

        <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
        <p v-else-if="hint" class="mt-1 text-sm text-gray-500">{{ hint }}</p>
    </div>
</template>

<script>
export default {
    name: 'AppInput',
    emits: ['update:modelValue', 'focus', 'blur'],
    props: {
        modelValue: [String, Number],
        type: {
            type: String,
            default: 'text'
        },
        label: String,
        placeholder: String,
        icon: String,
        error: String,
        hint: String,
        required: Boolean,
        disabled: Boolean
    },

    computed: {
        inputId() {
            return `input-${Math.random().toString(36).substr(2, 9)}`
        },

        inputClasses() {
            const base = 'block w-full px-3 py-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-0 transition-colors'
            const iconPadding = this.icon ? 'pl-10' : ''
            const state = this.error
                ? 'border-red-300 focus:border-red-500 focus:ring-red-500'
                : 'border-gray-300 focus:border-primary-500 focus:ring-primary-500'
            const disabled = this.disabled ? 'bg-gray-50 cursor-not-allowed' : 'bg-white'

            return [base, iconPadding, state, disabled].join(' ')
        }
    }
}
</script>