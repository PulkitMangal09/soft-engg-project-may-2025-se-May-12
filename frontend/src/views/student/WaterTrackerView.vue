<template>
    <div class="min-h-screen bg-gray-50 flex flex-col items-center py-6 px-2 md:px-0">
        <div class="text-4xl mb-2">💧</div>
        <div class="text-2xl font-bold text-blue-600 mb-1">6 / 8 Glasses</div>
        <div class="text-sm text-gray-600 mb-4">Daily Goal: 2000ml</div>
        <div class="bg-white rounded-xl shadow p-6 w-full max-w-md mb-4 flex flex-col items-center">
            <div class="flex gap-1 mb-2">
                <span v-for="i in 8" :key="i"
                    class="inline-block w-5 h-7 rounded-b bg-white border-2 border-blue-400 mr-1"
                    :class="{ 'bg-blue-400': i <= 6 }"></span>
            </div>
            <div class="text-sm text-gray-600 mb-2">75% Complete • 500ml remaining</div>
            <div class="grid grid-cols-3 gap-2 w-full mb-4">
                <button class="quick-add-btn bg-blue-50" @click="">🥤<div class='text-xs'>250ml Glass</div></button>
                <button class="quick-add-btn bg-blue-50" @click="">🍶<div class='text-xs'>500ml Bottle</div></button>
                <button class="quick-add-btn bg-blue-50" @click="">☕<div class='text-xs'>200ml Cup</div></button>
            </div>
            <div class="bg-gray-50 rounded-lg p-4 w-full mb-4">
                <div class="font-semibold mb-2">Today's Hydration Log</div>
                <div class="text-xs text-gray-700 space-y-1">
                    <div><span class="font-bold">8:00 AM</span> - 250ml (Glass of water)</div>
                    <div><span class="font-bold">10:30 AM</span> - 200ml (Coffee)</div>
                    <div><span class="font-bold">12:00 PM</span> - 250ml (Water with lunch)</div>
                    <div><span class="font-bold">2:00 PM</span> - 500ml (Water bottle)</div>
                    <div><span class="font-bold">4:30 PM</span> - 250ml (Herbal tea)</div>
                    <div><span class="font-bold">6:00 PM</span> - 250ml (Water with dinner)</div>
                </div>
            </div>
            <button class="btn-primary w-full mb-2">Add Custom Amount</button>
            <button class="btn-secondary w-full">Set Reminders</button>
        </div>
        <div class="text-xs text-gray-400 mt-4">Water Intake Tracker</div>
    </div>
</template>

<script setup>
// Placeholder logic for quick-add and hydration log
</script>