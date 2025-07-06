<template>
  <div class="flex flex-col h-screen bg-gray-50">

    <!-- Header -->
    <div class="px-4 py-3 border-b border-gray-200 flex items-center justify-between bg-white">
      <button class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100" @click="$router.go(-1)">
        ←
      </button>
      <h1 class="text-lg font-semibold">Mood Buddy</h1>
      <div class="w-8"></div> <!-- Spacer for alignment -->
    </div>

    <!-- Chat Container -->
    <div class="flex-1 overflow-y-auto p-4 space-y-4">
      <!-- System Message -->
      <div class="flex justify-start">
        <div class="max-w-xs bg-blue-100 text-blue-800 rounded-2xl p-3 text-sm">
          🤖 AI Support - This conversation is private and confidential
        </div>
      </div>

      <!-- User Message -->
      <div class="flex justify-end">
        <div class="max-w-xs bg-blue-500 text-white rounded-2xl p-3 text-sm">
          I've been feeling really stressed about school lately.
        </div>
      </div>

      <!-- Counselor Message -->
      <div class="flex justify-start">
        <div class="max-w-xs bg-gray-100 text-gray-800 rounded-2xl p-3 text-sm">
          I'm sorry to hear that. Would you like to talk more about what's been causing this stress?
        </div>
      </div>

      <!-- Typing Indicator -->
      <div class="flex justify-start">
        <div class="bg-gray-100 rounded-full p-2">
          <div class="flex space-x-1">
            <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0s"></div>
            <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Message Input -->
    <div class="border-t border-gray-200 bg-white p-3">
      <div class="flex items-center">
        <button class="p-2 text-gray-500 hover:text-gray-700">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </button>
        <input type="text" v-model="message" placeholder="Type a message..."
          class="flex-1 border border-gray-300 rounded-full py-2 px-4 mx-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          @keyup.enter="sendMessage">
        <button class="p-2 text-blue-500 hover:text-blue-700" @click="sendMessage">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const message = ref('');

const sendMessage = () => {
  if (message.value.trim()) {
    // In a real app, this would send the message to a server
    console.log('Sending message:', message.value);
    message.value = '';
  }
};
</script>

<style scoped>
.animate-bounce {
  animation: bounce 1.5s infinite;
}

@keyframes bounce {

  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-5px);
  }
}
</style>
