<template>
    <div class="min-h-screen bg-gray-50 flex flex-col items-center py-6 px-2 md:px-0">
        <div class="bg-white rounded-xl shadow p-6 w-full max-w-md mb-4">
            <div class="mb-4">
                <label class="block font-semibold mb-1">Weight (kg)</label>
                <input type="number" class="form-input w-full mb-3" placeholder="65.2" step="0.1">
                <label class="block font-semibold mb-1">Height (cm)</label>
                <input type="number" class="form-input w-full mb-3" placeholder="170" step="0.5">
            </div>
            <div class="bg-green-50 border-l-4 border-green-400 rounded-lg p-4 mb-4">
                <div class="font-semibold mb-2">Calculated BMI</div>
                <div class="text-2xl font-bold text-green-600 mb-1">22.6</div>
                <div class="text-sm text-gray-700">Normal Weight Range</div>
            </div>
            <div class="mb-4">
                <label class="block font-semibold mb-1">Blood Pressure</label>
                <div class="flex gap-2 mb-1">
                    <input type="number" class="form-input w-1/2" placeholder="120">
                    <span class="flex items-center font-bold">/</span>
                    <input type="number" class="form-input w-1/2" placeholder="80">
                </div>
                <div class="text-[10px] text-gray-500 mb-2">Systolic / Diastolic (mmHg)</div>
                <label class="block font-semibold mb-1">Blood Sugar (mg/dL)</label>
                <input type="number" class="form-input w-full mb-1" placeholder="110">
                <div class="text-[10px] text-gray-500 mb-2">Fasting: 70-100 | After meal: &lt;140</div>
                <label class="block font-semibold mb-1">Heart Rate (bpm)</label>
                <input type="number" class="form-input w-full mb-3" placeholder="72">
                <label class="block font-semibold mb-1">Notes</label>
                <textarea class="form-textarea w-full mb-3" placeholder="Any additional health notes..."></textarea>
            </div>
            <button class="btn-primary w-full mb-2">Save Metrics</button>
            <button class="btn-secondary w-full">Set Reminder</button>
        </div>
        <div class="text-xs text-gray-400 mt-4">Health Metrics Update</div>
    </div>
</template>

<script setup>
// Placeholder logic for save and reminder
</script>