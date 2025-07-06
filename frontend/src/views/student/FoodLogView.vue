<template>
    <div class="min-h-screen bg-gray-50 flex flex-col items-center py-6 px-2 md:px-0">
        <div class="w-full max-w-2xl">
            <div class="flex items-center justify-between mb-4">
                <button @click="$router.go(-1)"
                    class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100">←</button>
                <h2 class="text-lg font-bold">Today's Meals</h2>
                <div class="w-8 h-8"></div>
            </div>
            <FoodLog :meals="meals" />
        </div>
        <div class="text-xs text-gray-400 mt-4">Daily Food Log</div>
    </div>
</template>

<script setup>
import FoodLog from '@/components/diet/FoodLog.vue'
const meals = [
    {
        type: '🌅 Breakfast',
        icon: '🌅',
        totalCalories: 420,
        items: [
            { icon: '🥣', name: 'Oatmeal with Berries', quantity: '1 bowl', time: '8:30 AM', calories: 280 },
            { icon: '🥛', name: 'Milk (Low Fat)', quantity: '1 cup', time: '8:30 AM', calories: 140 },
        ]
    },
    {
        type: '🌞 Lunch',
        icon: '🌞',
        totalCalories: 580,
        items: [
            { icon: '🍗', name: 'Grilled Chicken Breast', quantity: '150g', time: '1:00 PM', calories: 350 },
            { icon: '🥗', name: 'Caesar Salad', quantity: '1 bowl', time: '1:00 PM', calories: 230 },
        ]
    },
    {
        type: '🍽️ Dinner',
        icon: '🍽️',
        totalCalories: 642,
        items: [
            { icon: '🍝', name: 'Spaghetti Marinara', quantity: '1 plate', time: '7:30 PM', calories: 480 },
            { icon: '🥖', name: 'Garlic Bread', quantity: '2 slices', time: '7:30 PM', calories: 162 },
        ]
    },
]
</script>