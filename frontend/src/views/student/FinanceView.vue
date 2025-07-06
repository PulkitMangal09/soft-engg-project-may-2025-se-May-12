<template>
  <div class="min-h-screen bg-gray-50">
    <StudentNavBar />
    <div class="p-4">
      <h1 class="text-2xl font-bold mb-4">Finance Management</h1>
      <p class="text-gray-600">Track your expenses and manage your budget</p>
      
      <!-- Placeholder content -->
      <div class="mt-8 bg-white p-6 rounded-xl shadow-sm">
        <div class="text-center py-8">
          <div class="text-gray-400 mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-700">Finance Dashboard</h3>
          <p class="text-gray-500 mt-1">Coming soon with expense tracking and budget management</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import StudentNavBar from '@/components/layout/StudentNavBar.vue'
// Future implementation for finance management
</script>
