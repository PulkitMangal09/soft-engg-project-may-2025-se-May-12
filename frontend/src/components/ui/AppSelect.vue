<template>
    <div class="form-group">
        <label v-if="label" :for="selectId" class="block text-sm font-medium text-gray-700 mb-2">
            {{ label }}
            <span v-if="required" class="text-red-500">*</span>
        </label>

        <select :id="selectId" :value="modelValue" :required="required" :disabled="disabled" :class="selectClasses"
            @change="$emit('update:modelValue', $event.target.value)">
            <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
            <option v-for="option in options" :key="getOptionValue(option)" :value="getOptionValue(option)">
                {{ getOptionLabel(option) }}
            </option>
        </select>

        <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
        <p v-else-if="hint" class="mt-1 text-sm text-gray-500">{{ hint }}</p>
    </div>
</template>

<script>
export default {
    name: 'AppSelect',
    emits: ['update:modelValue'],
    props: {
        modelValue: [String, Number],
        label: String,
        placeholder: String,
        options: {
            type: Array,
            required: true
        },
        valueKey: {
            type: String,
            default: 'value'
        },
        labelKey: {
            type: String,
            default: 'label'
        },
        error: String,
        hint: String,
        required: Boolean,
        disabled: Boolean
    },

    computed: {
        selectId() {
            return `select-${Math.random().toString(36).substr(2, 9)}`
        },

        selectClasses() {
            const base = 'block w-full px-3 py-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-0 transition-colors appearance-none bg-white'
            const state = this.error
                ? 'border-red-300 focus:border-red-500 focus:ring-red-500'
                : 'border-gray-300 focus:border-primary-500 focus:ring-primary-500'
            const disabled = this.disabled ? 'bg-gray-50 cursor-not-allowed' : ''

            return [base, state, disabled].join(' ')
        }
    },

    methods: {
        getOptionValue(option) {
            return typeof option === 'object' ? option[this.valueKey] : option
        },

        getOptionLabel(option) {
            return typeof option === 'object' ? option[this.labelKey] : option
        }
    }
}
</script>