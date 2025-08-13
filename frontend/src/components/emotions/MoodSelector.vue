<template>
  <div>
    <label class="block text-xl font-bold text-gray-800 mb-4">How are you feeling?</label>
    <div class="grid grid-cols-3 gap-4">
      <div v-for="mood in moods" :key="mood.name" @click="selectMood(mood.name)"
           class="flex flex-col items-center p-4 rounded-2xl cursor-pointer transition-all duration-300 transform border-2"
           :class="getMoodClasses(mood.name)">
        <span class="text-4xl transition-transform duration-300"
              :class="{'scale-125': selectedMood === mood.name}">
          {{ mood.icon }}
        </span>
        <span class="mt-2 text-sm font-semibold transition-colors duration-300"
              :class="{'text-white': selectedMood === mood.name, 'text-gray-700': selectedMood !== mood.name}">
          {{ mood.label }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits, defineProps, computed } from 'vue';

const props = defineProps({
  modelValue: String,
});

const emit = defineEmits(['update:modelValue']);

const selectedMood = ref(props.modelValue);

const moods = [
  { name: 'happy', label: 'Happy', icon: '😄', color: 'bg-yellow-400' },
  { name: 'sad', label: 'Sad', icon: '😢', color: 'bg-blue-400' },
  { name: 'angry', label: 'Angry', icon: '😠', color: 'bg-red-400' },
  { name: 'neutral', label: 'Neutral', icon: '😐', color: 'bg-gray-400' },
  { name: 'anxious', label: 'Anxious', icon: '😰', color: 'bg-purple-400' },
  { name: 'excited', label: 'Excited', icon: '🎉', color: 'bg-green-400' },
];

const getMoodClasses = (moodName) => {
  const isSelected = selectedMood.value === moodName;
  const mood = moods.find(m => m.name === moodName);
  
  if (isSelected) {
    return `${mood.color} text-white shadow-lg border-white`;
  } else {
    return 'bg-gray-100 hover:bg-gray-200 border-gray-200';
  }
};

const selectMood = (moodName) => {
  selectedMood.value = moodName;
  emit('update:modelValue', moodName);
};
</script>