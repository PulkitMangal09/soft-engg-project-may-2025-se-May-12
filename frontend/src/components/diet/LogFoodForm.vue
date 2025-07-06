<template>
    <div class="bg-white rounded-2xl shadow p-8">
        <h2 class="text-2xl font-bold mb-6">Log Food</h2>
        <form class="space-y-6" @submit.prevent="$emit('submit', form)">
            <div class="grid grid-cols-2 gap-6">
                <div>
                    <label class="block font-semibold mb-1">Meal Type</label>
                    <select v-model="form.mealType" class="form-select w-full">
                        <option>Breakfast</option>
                        <option>Lunch</option>
                        <option>Dinner</option>
                        <option>Snack</option>
                    </select>
                </div>
                <div>
                    <label class="block font-semibold mb-1">Food Item</label>
                    <input v-model="form.foodName" type="text" class="form-input w-full"
                        placeholder="Search or type food name">
                </div>
            </div>
            <div class="grid grid-cols-2 gap-6">
                <div>
                    <label class="block font-semibold mb-1">Quantity</label>
                    <div class="flex gap-2">
                        <input v-model.number="form.quantity" type="number" class="form-input w-1/3" placeholder="1">
                        <select v-model="form.unit" class="form-select w-2/3">
                            <option>Cup</option>
                            <option>Piece</option>
                            <option>Tablespoon</option>
                            <option>Grams</option>
                            <option>Bowl</option>
                        </select>
                    </div>
                </div>
                <div>
                    <label class="block font-semibold mb-1">Time</label>
                    <input v-model="form.time" type="time" class="form-input w-full">
                </div>
            </div>
            <div class="bg-emerald-50 border-l-4 border-emerald-400 rounded-lg p-4 text-xs">
                <div class="font-semibold mb-1">Nutritional Info (Estimated)</div>
                <div>
                    <strong>Calories:</strong> 245 • <strong>Carbs:</strong> 35g • <strong>Protein:</strong> 8g •
                    <strong>Fat:</strong> 12g<br>
                    <strong>Sodium:</strong> 450mg • <strong>Sugar:</strong> 15g • <strong>Fiber:</strong> 3g
                </div>
            </div>
            <div>
                <label class="block font-semibold mb-1">Notes</label>
                <textarea v-model="form.notes" class="form-textarea w-full"
                    placeholder="Any additional notes about this meal..."></textarea>
            </div>
            <div class="flex gap-4">
                <button class="btn-primary" type="submit">Log Food</button>
                <button class="btn-secondary" type="button">📷 Take Photo</button>
            </div>
        </form>
    </div>
</template>
<script setup>
import { reactive, watch } from 'vue'
const props = defineProps({
    modelValue: Object
})
const form = reactive({
    mealType: 'Breakfast',
    foodName: '',
    quantity: 1,
    unit: 'Cup',
    time: '12:30',
    notes: ''
})
watch(() => props.modelValue, (val) => {
    if (val) Object.assign(form, val)
}, { immediate: true })
</script>