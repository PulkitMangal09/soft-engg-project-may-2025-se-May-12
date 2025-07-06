<template>
  <div class="bg-white border border-gray-200 rounded-xl p-4 mb-4 shadow-sm hover:shadow-md transition-shadow">
    <div class="flex justify-between items-start mb-2">
      <div>
        <h3 class="font-medium text-gray-900">{{ entry.title }}</h3>
        <p class="text-xs text-gray-500">{{ formattedDate }}</p>
      </div>
      <div class="flex space-x-2">
        <button 
          @click.stop="$emit('edit', entry)" 
          class="text-gray-400 hover:text-blue-500 p-1"
          aria-label="Edit entry"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        </button>
        <button 
          @click.stop="confirmDelete" 
          class="text-gray-400 hover:text-red-500 p-1"
          aria-label="Delete entry"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>
    </div>
    
    <p class="text-gray-700 text-sm mb-3 whitespace-pre-line">{{ entry.content }}</p>
    
    <div v-if="entry.tags && entry.tags.length" class="flex flex-wrap gap-2">
      <span 
        v-for="(tag, index) in entry.tags" 
        :key="index"
        class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
      >
        {{ tag }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  entry: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['edit', 'delete']);

const formattedDate = computed(() => {
  return new Date(props.entry.date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
});

const confirmDelete = () => {
  if (confirm('Are you sure you want to delete this diary entry?')) {
    emit('delete', props.entry.id);
  }
};
</script>
