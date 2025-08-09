<template>
    <div class="min-h-screen bg-gray-50 flex flex-col items-center py-6 px-2 md:px-0">
        <div class="text-4xl mb-2">💧</div>
        <div class="text-2xl font-bold text-blue-600 mb-1">{{ glasses }} / 8 Glasses</div>
        <div class="text-sm text-gray-600 mb-4">Total: {{ totalMl }} ml</div>
        <div class="bg-white rounded-xl shadow p-6 w-full max-w-md mb-4 flex flex-col items-center">
            <div class="flex gap-1 mb-2">
                <span v-for="i in 8" :key="i"
                    class="inline-block w-5 h-7 rounded-b bg-white border-2 border-blue-400 mr-1"
                    :class="{ 'bg-blue-400': i <= glasses }"></span>
            </div>
            <div class="grid grid-cols-3 gap-2 w-full mb-4">
                <button class="quick-add-btn bg-blue-50" @click="quickAdd(250)">🥤<div class='text-xs'>250ml Glass</div>
                </button>
                <button class="quick-add-btn bg-blue-50" @click="quickAdd(500)">🍶<div class='text-xs'>500ml Bottle
                    </div></button>
                <button class="quick-add-btn bg-blue-50" @click="quickAdd(200)">☕<div class='text-xs'>200ml Cup</div>
                </button>
            </div>
            <div class="bg-gray-50 rounded-lg p-4 w-full mb-4">
                <div class="font-semibold mb-2">Today's Hydration Log</div>
                <div class="text-xs text-gray-700 space-y-1">
                    <div v-for="l in logs" :key="l.intake_id"><span class="font-bold">{{ formatTime(l.intake_time)
                    }}</span> - {{ l.amount_ml }}ml ({{ l.container_type }})</div>
                </div>
            </div>
            <button class="btn-primary w-full mb-2" @click="customAdd">Add Custom Amount</button>
            <button class="btn-secondary w-full" @click="refresh">Refresh</button>
        </div>
        <div class="text-xs text-gray-400 mt-4">Water Intake Tracker</div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getWaterSummary, addWater, getWaterLogs } from '@/services/waterService'

const glasses = ref(0)
const totalMl = ref(0)
const logs = ref([])

function formatTime(t) {
    if (!t) return ''
    return t.slice(0, 5)
}

async function refresh() {
    const s = await getWaterSummary()
    totalMl.value = s.total_ml || 0
    glasses.value = Math.min(8, Math.round(totalMl.value / 250))
    logs.value = await getWaterLogs()
}

async function quickAdd(ml) {
    await addWater(ml, ml >= 500 ? 'bottle' : ml >= 250 ? 'glass' : 'cup')
    await refresh()
}

async function customAdd() {
    const ml = parseInt(prompt('Enter amount (ml):') || '0', 10)
    if (ml > 0) {
        await addWater(ml, ml >= 500 ? 'bottle' : ml >= 250 ? 'glass' : 'cup')
        await refresh()
    }
}

onMounted(refresh)
</script>