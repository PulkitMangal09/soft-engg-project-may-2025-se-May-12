<template>
  <div class="min-h-screen bg-gray-50">
    <StudentNavBar />
    <div class="p-4 max-w-md mx-auto">
      <div class="flex items-center mb-6">
        <router-link to="/student/emotion" class="mr-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </router-link>
        <h1 class="text-2xl font-bold">New Emotion Entry</h1>
      </div>

      <form @submit.prevent="submitEntry">
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
            rows="5"
            class="w-full p-2 border border-gray-300 rounded-lg focus:ring-red-500 focus:border-red-500"
            placeholder="Describe your feelings, what happened today..."
          ></textarea>
        </div>

        <div class="mb-6">
          <label for="tags" class="block text-sm font-medium text-gray-700 mb-2">Add tags (e.g., school, friends, exam)</label>
          <input
            type="text"
            id="tags"
            v-model="tagsInput"
            @keydown.enter.prevent="addTag"
            class="w-full p-2 border border-gray-300 rounded-lg focus:ring-red-500 focus:border-red-500"
            placeholder="Type a tag and press Enter"
          />
          <div class="flex flex-wrap gap-2 mt-2">
            <span v-for="(tag, index) in entry.tags" :key="index" class="bg-red-100 text-red-700 text-xs font-medium px-2.5 py-1 rounded-full flex items-center">
              {{ tag }}
              <button @click="removeTag(index)" class="ml-1.5 text-red-700 hover:text-red-900">
                &times;
              </button>
            </span>
          </div>
        </div>

        <button type="submit" class="w-full bg-red-500 text-white font-bold py-3 px-4 rounded-lg hover:bg-red-600 transition-colors">
          Save Entry
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import StudentNavBar from '@/components/layout/StudentNavBar.vue'
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import MoodSelector from '@/components/emotions/MoodSelector.vue';

const router = useRouter();

const entry = ref({
  mood: 'neutral',
  intensity: 7, // Default to moderate
  text: '',
  tags: [],
  date: new Date().toISOString()
});

const intensityLabels = ['Mild', 'Moderate', 'Intense'];

const tagsInput = ref('');

const addTag = () => {
  const newTag = tagsInput.value.trim();
  if (newTag && !entry.value.tags.includes(newTag)) {
    entry.value.tags.push(newTag);
  }
  tagsInput.value = '';
};

const removeTag = (index) => {
  entry.value.tags.splice(index, 1);
};

const submitEntry = () => {
  console.log('Submitting new entry:', entry.value);
  // Here you would typically call a store action or API to save the data
  // For now, we'll just navigate back
  router.push('/student/emotion');
};
</script>
