<template>
  <div class="p-4">
    <div class="flex items-center mb-6">
      <router-link to="/student/emotion" class="mr-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </router-link>
      <h1 class="text-2xl font-bold">All Diary Entries</h1>
    </div>

    <div class="space-y-4">
      <DiaryCard 
        v-for="entry in diaryEntries" 
        :key="entry.id" 
        :entry="entry"
        @edit="handleEditEntry"
        @delete="handleDeleteEntry"
      />
    </div>

    <div v-if="diaryEntries.length === 0" class="text-center text-gray-500 mt-10">
      <p>No entries yet.</p>
      <router-link 
        to="/student/emotion/new" 
        class="mt-4 inline-block bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors"
      >
        Create Your First Entry
      </router-link>
    </div>
  </div>

  <!-- Confirmation Dialog -->
  <div v-if="showDeleteDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-xl p-6 w-full max-w-md">
      <h3 class="text-lg font-semibold mb-4">Delete Entry</h3>
      <p class="text-gray-600 mb-6">Are you sure you want to delete this entry? This action cannot be undone.</p>
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
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import DiaryCard from '@/components/emotions/DiaryCard.vue';

const router = useRouter();

// State
const showDeleteDialog = ref(false);
const entryToDelete = ref(null);

// Mock data - replace with API call later
const diaryEntries = ref([
  { 
    id: 1, 
    mood: 'happy', 
    text: 'Had a great day at school.', 
    tags: ['school', 'friends'], 
    date: '2025-07-02T10:00:00Z',
    intensity: 8,
    whatHelped: 'Talking to friends, going for a walk'
  },
  { 
    id: 2, 
    mood: 'anxious', 
    text: 'Worried about the upcoming exam.', 
    tags: ['exam', 'stress'], 
    date: '2025-07-01T18:30:00Z',
    intensity: 6,
    whatHelped: 'Studying with a friend, taking breaks'
  },
  { 
    id: 3, 
    mood: 'excited', 
    text: 'Family trip this weekend!', 
    tags: ['family', 'vacation'], 
    date: '2025-06-30T15:00:00Z',
    intensity: 9,
    whatHelped: 'Planning activities, packing early'
  },
  { 
    id: 4, 
    mood: 'sad', 
    text: 'Missed my friends today.', 
    tags: ['friends'], 
    date: '2025-06-29T20:00:00Z',
    intensity: 5,
    whatHelped: 'Video calling a friend, watching a movie'
  },
  { 
    id: 5, 
    mood: 'calm', 
    text: 'A peaceful evening reading a book.', 
    tags: ['reading', 'relax'], 
    date: '2025-06-28T21:00:00Z',
    intensity: 3,
    whatHelped: 'Reading, drinking tea, soft music'
  },
]);

// Handle edit entry
const handleEditEntry = (entry) => {
  router.push({ 
    name: 'EditEmotionEntry', 
    params: { id: entry.id },
    state: { entry } // Pass the entry data to the edit view
  });
};

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
