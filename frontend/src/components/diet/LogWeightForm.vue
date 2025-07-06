<template>
    <div class="bg-white rounded-2xl shadow p-8">
        <h2 class="text-2xl font-bold mb-6">Log Weight</h2>
        <form @submit.prevent="$emit('submit', weight)">
            <label class="block font-semibold mb-1">Weight (kg)</label>
            <input v-model.number="weight" type="number" class="form-input w-full mb-4" placeholder="e.g. 60">
            <button class="btn-primary w-full" type="submit">Save</button>
        </form>
    </div>
</template>
<script setup>
import { ref } from 'vue'
const weight = ref(60)
</script>