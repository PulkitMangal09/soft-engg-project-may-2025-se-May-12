<template>
  <div class="p-4">
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center">
        <router-link to="/student/emotion" class="mr-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </router-link>
        <h1 class="text-2xl font-bold">My Diary</h1>
      </div>
      <router-link 
        to="/student/diary/new" 
        class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        New Entry
      </router-link>
    </div>

    <div v-if="isLoading" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>

    <div v-else>
      <div v-if="diaryEntries.length === 0" class="text-center mt-16">
        <div class="text-gray-400 mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">No diary entries yet</h3>
        <p class="text-gray-500 mb-6">Start journaling your thoughts and experiences.</p>
        <router-link 
          to="/student/diary/new" 
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Write your first entry
        </router-link>
      </div>

      <div v-else class="space-y-4">
        <DiaryCard 
          v-for="entry in diaryEntries" 
          :key="entry.id" 
          :entry="entry"
          @edit="handleEditEntry"
          @delete="handleDeleteEntry"
        />
      </div>
    </div>
  </div>

  <!-- Delete Confirmation Dialog -->
  <div v-if="showDeleteDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-xl p-6 w-full max-w-md">
      <h3 class="text-lg font-semibold mb-4">Delete Entry</h3>
      <p class="text-gray-600 mb-6">Are you sure you want to delete this diary entry? This action cannot be undone.</p>
      <div class="flex justify-end space-x-3">
        <button 
          @click="showDeleteDialog = false" 
          class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
        >
          Cancel
        </button>
        <button 
          @click="confirmDelete" 
          class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
        >
          Delete
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import DiaryCard from '@/components/diary/DiaryCard.vue';

const router = useRouter();

// State
const isLoading = ref(true);
const showDeleteDialog = ref(false);
const entryToDelete = ref(null);

// Mock data - replace with API call
const diaryEntries = ref([
  {
    id: '1',
    title: 'A Great Day at School',
    content: 'Today was amazing! I aced my math test and had so much fun during lunch with my friends. We sat outside since the weather was perfect. I feel really happy and proud of myself for studying hard.',
    tags: ['school', 'friends', 'achievement'],
    date: '2025-07-01T15:30:00Z'
  },
  {
    id: '2',
    title: 'Weekend Plans',
    content: 'Thinking about what to do this weekend. Maybe I should go hiking or visit the new cafe that opened downtown. I need to finish my homework first though!',
    tags: ['weekend', 'plans', 'free time'],
    date: '2025-06-30T19:15:00Z'
  },
  {
    id: '3',
    title: 'Book Recommendation',
    content: 'Just finished reading "The Midnight Library" by Matt Haig. It was such an inspiring book about choices and second chances. Made me think a lot about my own life and the paths I\'m taking.',
    tags: ['books', 'reading', 'reflection'],
    date: '2025-06-28T21:45:00Z'
  }
]);

// Lifecycle hook
onMounted(() => {
  // Simulate loading
  setTimeout(() => {
    isLoading.value = false;
  }, 500);
});

// Handle edit entry
const handleEditEntry = (entry) => {
  router.push({ 
    name: 'EditDiaryEntry', 
    params: { id: entry.id },
    state: { entry }
  });};

// Handle delete entry
const handleDeleteEntry = (entryId) => {
  entryToDelete.value = entryId;
  showDeleteDialog.value = true;
};

// Confirm delete
const confirmDelete = () => {
  if (entryToDelete.value) {
    // In a real app, this would be an API call
    const index = diaryEntries.value.findIndex(entry => entry.id === entryToDelete.value);
    if (index !== -1) {
      diaryEntries.value.splice(index, 1);
    }
  }
  showDeleteDialog.value = false;
  entryToDelete.value = null;
};
</script>
