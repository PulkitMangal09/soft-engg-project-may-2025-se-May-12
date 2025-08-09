<template>
  <div class="p-4">
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center">
        <router-link to="/student/emotion" class="mr-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </router-link>
        <h1 class="text-2xl font-bold">My Diary</h1>
      </div>
      <router-link to="/student/diary/new"
        class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24"
          stroke="currentColor">
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
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">No diary entries yet</h3>
        <p class="text-gray-500 mb-6">Start journaling your thoughts and experiences.</p>
        <router-link to="/student/diary/new"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
          Write your first entry
        </router-link>
      </div>

      <div v-else class="space-y-4">
        <DiaryCard v-for="entry in diaryEntries" :key="entry.id" :entry="entry" @edit="handleEditEntry"
          @delete="handleDeleteEntry" />
      </div>
    </div>
  </div>

  <!-- Delete Confirmation Dialog -->
  <div v-if="showDeleteDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-xl p-6 w-full max-w-md">
      <h3 class="text-lg font-semibold mb-4">Delete Entry</h3>
      <p class="text-gray-600 mb-6">Are you sure you want to delete this diary entry? This action cannot be undone.</p>
      <div class="flex justify-end space-x-3">
        <button @click="showDeleteDialog = false" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
          Cancel
        </button>
        <button @click="confirmDelete" class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600">
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
