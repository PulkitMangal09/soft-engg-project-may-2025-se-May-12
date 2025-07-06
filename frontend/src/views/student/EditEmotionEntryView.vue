<template>
  <div class="p-4 max-w-md mx-auto">
    <div class="flex items-center mb-6">
      <button @click="$router.go(-1)" class="mr-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      <h1 class="text-2xl font-bold">Edit Entry</h1>
    </div>

    <form @submit.prevent="updateEntry">
      <div class="mb-6">
        <MoodSelector v-model="entry.mood" />
      </div>

      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-700 mb-2">Intensity (1-10)</label>
        <div class="relative">
          <input 
            type="range" 
            v-model="entry.intensity"
            min="1" 
            max="10" 
            class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            :style="{
              'background': `linear-gradient(to right, #3b82f6 0%, #3b82f6 ${(entry.intensity - 1) * 11.11}%, #e5e7eb ${(entry.intensity - 1) * 11.11}%, #e5e7eb 100%)`
            }"
          >
          <div class="flex justify-between text-xs text-gray-500 mt-1 px-1">
            <span>Mild</span>
            <span>Moderate</span>
            <span>Intense</span>
          </div>
        </div>
        <div class="mt-2 text-center text-sm font-medium text-blue-600">
          {{ intensityLabels[Math.min(Math.max(1, Math.ceil(entry.intensity / 3.33)), 3) - 1] }}
        </div>
      </div>

      <div class="mb-6">
        <label for="entry-text" class="block text-sm font-medium text-gray-700 mb-2">What's on your mind?</label>
        <textarea
          id="entry-text"
          v-model="entry.text"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
          rows="4"
          placeholder="Describe your feelings..."
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
import MoodSelector from '@/components/emotions/MoodSelector.vue';

const route = useRoute();
const router = useRouter();

// In a real app, this would be fetched from the store/API
const entry = ref({
  id: null,
  mood: 'neutral',
  intensity: 7,
  text: '',
  tags: [],
  date: new Date().toISOString()
});

const newTag = ref('');
const intensityLabels = ['Mild', 'Moderate', 'Intense'];

// Load entry data (in a real app, this would be from an API)
const loadEntry = () => {
  // This is a mock - in a real app, you would fetch the entry by ID
  const mockEntry = {
    id: route.params.id,
    mood: 'happy',
    intensity: 7,
    text: 'Had a great day at school today!',
    tags: ['school', 'friends'],
    date: new Date().toISOString()
  };
  
  // In a real app, you would check if the entry exists and handle 404
  Object.assign(entry.value, mockEntry);
};

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
  console.log('Updating entry:', entry.value);
  
  // Show success message and navigate back
  alert('Entry updated successfully!');
  router.push('/student/emotion');
};

// Load the entry when the component is mounted
onMounted(() => {
  loadEntry();
});
</script>
