<template>
    <div class="bg-gradient-to-r from-blue-400 to-blue-600 rounded-xl p-6 text-white text-center">
        <div class="font-semibold mb-3 text-lg">Daily Water Intake</div>
        <div class="flex justify-center gap-3 mb-3">
            <button v-for="i in 8" :key="i" @click="$emit('update', i)"
                :class="['w-8 h-12 border-2 rounded-b-lg relative transition', i <= modelValue ? 'bg-white border-white' : 'border-white/60', 'hover:scale-110']">
                <span class="absolute left-0 right-0 top-0 h-2 rounded-t bg-white/60"
                    :class="i <= modelValue ? 'bg-white' : ''"></span>
            </button>
        </div>
        <div class="text-sm opacity-90">{{ modelValue }} of 8 glasses complete</div>
    </div>
</template>
<script setup>
defineProps({
    modelValue: {
        type: Number,
        required: true
    }
});
</script>