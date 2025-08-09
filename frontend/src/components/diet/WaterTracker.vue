<template>
    <div class="bg-gradient-to-r from-blue-400 to-blue-600 rounded-xl p-6 text-white text-center">
        <div class="font-semibold mb-3 text-lg">Daily Water Intake</div>
        <div class="flex justify-center gap-3 mb-3">
            <button v-for="i in 8" :key="i" @click="updateTo(i)"
                :class="['w-8 h-12 border-2 rounded-b-lg relative transition', i <= internal ? 'bg-white border-white' : 'border-white/60', 'hover:scale-110']">
                <span class="absolute left-0 right-0 top-0 h-2 rounded-t bg-white/60"
                    :class="i <= internal ? 'bg-white' : ''"></span>
            </button>
        </div>
        <div class="text-sm opacity-90">{{ internal }} of 8 glasses complete</div>
        <div class="mt-3 grid grid-cols-3 gap-2">
            <button class="bg-white/20 rounded-lg py-2" @click="quickAdd(250)">🥤 250ml</button>
            <button class="bg-white/20 rounded-lg py-2" @click="quickAdd(500)">🍶 500ml</button>
            <button class="bg-white/20 rounded-lg py-2" @click="quickAdd(200)">☕ 200ml</button>
        </div>
    </div>
</template>
<script setup>
import { ref, watch, defineProps, defineEmits } from 'vue'

const props = defineProps({ modelValue: { type: Number, required: true } })
const emit = defineEmits(['update:modelValue', 'add'])

const internal = ref(props.modelValue)
watch(() => props.modelValue, v => { internal.value = v })

function updateTo(i) {
    internal.value = i
    emit('update:modelValue', i)
}

function quickAdd(ml) {
    emit('add', ml)
}
</script>