<template>
    <div class="h-40 relative">
        <div class="absolute bottom-0 w-full flex justify-between items-end h-32 px-1">
            <div v-for="(stat, index) in statsData" :key="index" class="flex-1 flex flex-col items-center">
                <div class="w-6 rounded-t bg-emerald-400" :style="{ height: `${stat.value * 2}px` }"></div>
                <span class="text-xs text-gray-500 mt-1">{{ stat.label }}</span>
            </div>
        </div>
    </div>
</template>

<script setup>
const statsData = [
    { label: 'Cal', value: 18 },
    { label: 'Carb', value: 16 },
    { label: 'Prot', value: 8 },
    { label: 'Fat', value: 10 },
];
</script>