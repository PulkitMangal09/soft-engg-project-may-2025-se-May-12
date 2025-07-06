<template>
    <div class="bg-white rounded-2xl shadow p-8">
        <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-bold">Today's Meals</h2>
            <slot name="add"></slot>
        </div>
        <div class="grid grid-cols-4 gap-4 mb-6">
            <div class="bg-gray-50 rounded-xl p-4 text-center">
                <div class="text-xl font-bold text-emerald-500">1,842</div>
                <div class="text-xs text-gray-500">Total Calories</div>
            </div>
            <div class="bg-gray-50 rounded-xl p-4 text-center">
                <div class="text-xl font-bold text-emerald-500">158g</div>
                <div class="text-xs text-gray-500">Carbs</div>
            </div>
            <div class="bg-gray-50 rounded-xl p-4 text-center">
                <div class="text-xl font-bold text-emerald-500">68g</div>
                <div class="text-xs text-gray-500">Protein</div>
            </div>
            <div class="bg-gray-50 rounded-xl p-4 text-center">
                <div class="text-xl font-bold text-emerald-500">82g</div>
                <div class="text-xs text-gray-500">Fat</div>
            </div>
        </div>
        <div>
            <div v-for="meal in meals" :key="meal.type" class="mb-6">
                <div class="flex items-center justify-between bg-gray-100 rounded-lg px-4 py-2 mb-2">
                    <div class="font-semibold">{{ meal.icon }} {{ meal.type }}</div>
                    <div class="text-emerald-600 font-semibold text-sm">{{ meal.totalCalories }} cal</div>
                </div>
                <div v-for="item in meal.items" :key="item.name"
                    class="flex items-center bg-white rounded-lg p-4 mb-2 shadow">
                    <div class="w-12 h-12 rounded-lg bg-gray-100 flex items-center justify-center text-2xl mr-4">{{
                        item.icon }}</div>
                    <div class="flex-1">
                        <div class="font-semibold text-base">{{ item.name }}</div>
                        <div class="text-xs text-gray-400">{{ item.quantity }} • {{ item.time }}</div>
                    </div>
                    <div class="font-semibold text-emerald-500">{{ item.calories }} cal</div>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
defineProps({
    meals: {
        type: Array,
        required: true
    }
});
</script>