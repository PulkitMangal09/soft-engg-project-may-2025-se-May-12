<template>
  <div class="p-4 max-w-md mx-auto">
    <div class="flex items-center mb-6">
      <button @click="$router.go(-1)" class="mr-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      <h1 class="text-2xl font-bold">Edit Diary Entry</h1>
    </div>

    <form @submit.prevent="updateEntry">
      <div class="mb-6">
        <label for="entry-title" class="block text-sm font-medium text-gray-700 mb-2">Title</label>
        <input
          id="entry-title"
          v-model="entry.title"
          type="text"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
          placeholder="Give your entry a title"
          required
        >
      </div>

      <div class="mb-6">
        <label for="entry-text" class="block text-sm font-medium text-gray-700 mb-2">What's on your mind?</label>
        <textarea
          id="entry-text"
          v-model="entry.content"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
          rows="8"
          placeholder="Write about your day, thoughts, or anything you'd like to remember..."
          required
        ></textarea>
      </div>

      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-700 mb-2">Tags (press Enter to add)</label>
        <div class="flex flex-wrap gap-2 mb-2">
          <span 
            v-for="(tag, index) in entry.tags" 
            :key="index"
            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
          >
            {{ tag }}
            <button 
              type="button" 
              @click="removeTag(index)"
              class="ml-1.5 inline-flex items-center justify-center w-3.5 h-3.5 rounded-full text-blue-400 hover:bg-blue-200 hover:text-blue-500"
            >
              ×
            </button>
          </span>
        </div>
        <input
          type="text"
          v-model="newTag"
          @keydown.enter.prevent="addTag"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
          placeholder="Add a tag and press Enter"
        >
      </div>

      <div class="flex space-x-4">
        <button
          type="submit"
          class="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Update Entry
        </button>
        <button
          type="button"
          @click="$router.go(-1)"
          class="flex-1 border border-gray-300 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
        >
          Cancel
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

// Entry data
const entry = ref({
  id: null,
  title: '',
  content: '',
  tags: [],
  date: new Date().toISOString()
});

const newTag = ref('');

// Load entry data
const loadEntry = () => {
  // In a real app, this would fetch from an API
  const mockEntry = {
    id: route.params.id,
    title: 'A Great Day at School',
    content: 'Today was amazing! I aced my math test and had so much fun during lunch with my friends. We sat outside since the weather was perfect. I feel really happy and proud of myself for studying hard.',
    tags: ['school', 'friends', 'achievement'],
    date: '2025-07-01T15:30:00Z'
  };
  
  // In a real app, you would check if the entry exists and handle 404
  Object.assign(entry.value, mockEntry);};

const addTag = () => {
  if (newTag.value.trim() && !entry.value.tags.includes(newTag.value.trim())) {
    entry.value.tags.push(newTag.value.trim());
    newTag.value = '';
  }
};

const removeTag = (index) => {
  entry.value.tags.splice(index, 1);
};

const updateEntry = () => {
  // In a real app, this would update the entry in the store/API
  console.log('Updating diary entry:', entry.value);
  
  // Show success message and navigate back
  alert('Diary entry updated successfully!');
  router.push('/student/diary');
};

// Load the entry when the component is mounted
onMounted(() => {
  loadEntry();
});
</script>
