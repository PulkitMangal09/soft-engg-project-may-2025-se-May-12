<template>
  <div class="flex flex-col items-center justify-center min-h-[60vh] bg-gradient-to-br from-indigo-200 via-purple-100 to-pink-100 rounded-3xl shadow-lg p-10 mx-auto max-w-xl mt-16">
    <h1 class="text-4xl font-extrabold text-indigo-700 mb-4 drop-shadow-lg">Welcome to <span class="text-purple-600">GrowthGeine</span> Home!</h1>
    <p class="text-lg text-gray-700 mb-2">This is the home page.</p>
    <div class="mt-6 flex gap-4">
      <button class="px-6 py-2 rounded-lg bg-indigo-600 text-white font-semibold shadow hover:bg-indigo-700 transition">Get Started</button>
      <button class="px-6 py-2 rounded-lg bg-white border border-indigo-300 text-indigo-700 font-semibold shadow hover:bg-indigo-50 transition">Learn More</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
}
</script>

<style scoped>
.home-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 40px;
}
</style> 