<template>
  <div class="min-h-screen bg-gray-50 p-6 sm:p-8">
    <div class="flex items-center justify-between mb-8">
      <div class="flex items-center">
        <router-link to="/student/emotion" class="mr-4 text-gray-500 hover:text-blue-600 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </router-link>
        <h1 class="text-3xl font-extrabold text-gray-900">My Diary</h1>
      </div>
      <div class="hidden sm:block">
        <button class="flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white rounded-lg shadow-sm hover:bg-gray-100">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <span class="hidden md:inline">August 2025</span>
        </button>
      </div>
    </div>

    <div v-if="isLoading" class="flex justify-center items-center h-96">
      <svg class="animate-spin h-10 w-10 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>

    <div v-else>
      <div v-if="diaryEntries.length === 0" class="text-center mt-20">
        <div class="text-gray-300 mb-6">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 mx-auto" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3 class="text-2xl font-bold text-gray-900 mb-2">Nothing here yet</h3>
        <p class="text-gray-500 mb-6 max-w-sm mx-auto">Start your journaling journey by writing down your thoughts and experiences. Your entries are private and secure.</p>
        <router-link to="/student/diary/new"
          class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-xl shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
          Write your first entry
        </router-link>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <DiaryCard v-for="entry in diaryEntries" :key="entry.id" :entry="entry" @edit="handleEditEntry" @delete="handleDeleteEntry" />
      </div>
    </div>
    
    <router-link to="/student/diary/new" class="fixed bottom-6 right-6 p-4 bg-blue-600 text-white rounded-full shadow-lg hover:bg-blue-700 transition-colors">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
      </svg>
    </router-link>
  </div>

  <div v-if="showDeleteDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-2xl p-8 w-full max-w-md shadow-xl">
      <h3 class="text-xl font-bold mb-4 text-gray-900">Confirm Deletion</h3>
      <p class="text-gray-600 mb-6">Are you sure you want to permanently delete this diary entry? This action cannot be undone.</p>
      <div class="flex justify-end space-x-3">
        <button @click="showDeleteDialog = false" class="px-5 py-2 text-gray-600 font-medium rounded-lg hover:bg-gray-100 transition-colors">
          Cancel
        </button>
        <button @click="confirmDelete" class="px-5 py-2 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 transition-colors">
          Delete
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import DiaryCard from '@/components/diary/DiaryCard.vue'
import { listDiaryEntries, deleteDiaryEntry } from '@/services/diaryService'

const router = useRouter()

const isLoading = ref(true)
const showDeleteDialog = ref(false)
const entryToDelete = ref(null)
const diaryEntries = ref([])

onMounted(async () => {
  await loadEntries()
})

async function loadEntries() {
  isLoading.value = true
  try {
    diaryEntries.value = await listDiaryEntries()
  } finally {
    isLoading.value = false
  }
}

function handleEditEntry(entry) {
  router.push({ name: 'EditDiaryEntry', params: { id: entry.id }, state: { entry } })
}

function handleDeleteEntry(entryId) {
  entryToDelete.value = entryId
  showDeleteDialog.value = true
}

async function confirmDelete() {
  if (entryToDelete.value) {
    await deleteDiaryEntry(entryToDelete.value)
    diaryEntries.value = diaryEntries.value.filter(e => e.id !== entryToDelete.value)
  }
  showDeleteDialog.value = false
  entryToDelete.value = null
}
</script>
