<template>
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-2">How are you feeling?</label>
    <div class="flex justify-around p-3 bg-gray-100 rounded-lg">
      <div v-for="mood in moods" :key="mood.name" @click="selectMood(mood.name)"
        class="text-3xl cursor-pointer p-2 rounded-full transition-transform transform"
        :class="{ 'bg-red-200 scale-110': selectedMood === mood.name }">
        {{ mood.icon }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits, defineProps } from 'vue';

const props = defineProps({
  modelValue: String,
});

const emit = defineEmits(['update:modelValue']);

const selectedMood = ref(props.modelValue);

const moods = [
  { name: 'happy', icon: '😄' },
  { name: 'sad', icon: '😢' },
  { name: 'angry', icon: '😠' },
  { name: 'neutral', icon: '😐' },
  { name: 'anxious', icon: '😰' },
  { name: 'excited', icon: '🎉' },
];

const selectMood = (moodName) => {
  selectedMood.value = moodName;
  emit('update:modelValue', moodName);
};
</script>
