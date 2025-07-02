<template>
  <div class="p-4 flex flex-col items-center justify-center h-screen bg-blue-50">
    <div class="flex items-center mb-8 absolute top-4 left-4">
      <router-link to="/student/emotion" class="mr-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </router-link>
    </div>

    <h1 class="text-2xl font-bold mb-4">Breathing Exercise</h1>
    <p class="text-gray-600 mb-8">Follow the animation and breathe.</p>

    <div class="relative w-48 h-48 flex items-center justify-center">
      <div class="absolute w-full h-full bg-blue-300 rounded-full animate-pulse-slow"></div>
      <div class="relative w-32 h-32 bg-blue-400 rounded-full flex items-center justify-center text-white font-bold text-lg shadow-lg">
        {{ instruction }}
      </div>
    </div>

    <div class="mt-8 text-lg font-semibold">
      <p>Round: {{ round }} / 5</p>
    </div>

    <button @click="toggleAnimation" class="mt-6 bg-white text-blue-500 font-bold py-2 px-6 rounded-full shadow-md hover:bg-blue-100 transition-colors">
      {{ isRunning ? 'Pause' : 'Start' }}
    </button>
  </div>
</template>

<script setup>
import { ref, watch, onUnmounted } from 'vue';

const instruction = ref('Breathe In');
const round = ref(0);
const isRunning = ref(false);
let intervalId = null;

const instructions = ['Breathe In', 'Hold', 'Breathe Out', 'Hold'];
let instructionIndex = 0;

const cycle = () => {
  instruction.value = instructions[instructionIndex % 4];
  if (instructionIndex % 4 === 0) {
    const currentRound = Math.floor(instructionIndex / 4) + 1;
    if (currentRound > 5) {
      reset();
      return;
    }
    round.value = currentRound;
  }
  instructionIndex++;
};

const start = () => {
  if (round.value === 0) round.value = 1;
  intervalId = setInterval(cycle, 4000); // 4 seconds per instruction
  isRunning.value = true;
};

const pause = () => {
  clearInterval(intervalId);
  isRunning.value = false;
};

const reset = () => {
  pause();
  round.value = 0;
  instructionIndex = 0;
  instruction.value = 'Breathe In';
}

const toggleAnimation = () => {
  if (isRunning.value) {
    pause();
  } else {
    start();
  }
};

onUnmounted(() => {
  clearInterval(intervalId);
});

</script>

<style scoped>
@keyframes pulse-slow {
  0%, 100% {
    transform: scale(1);
    opacity: 0.7;
  }
  50% {
    transform: scale(1.1);
    opacity: 1;
  }
}

.animate-pulse-slow {
  animation: pulse-slow 8s infinite;
}
</style>
