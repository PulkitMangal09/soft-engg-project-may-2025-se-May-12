<template>
  <div class="flex flex-col h-screen bg-gray-50">
    <!-- Header -->
    <div class="px-4 py-3 border-b border-gray-200 flex items-center justify-between bg-white">
      <button class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100" @click="$router.go(-1)">
        ←
      </button>
      <h1 class="text-lg font-semibold">Emergency Help</h1>
      <div class="w-8"></div> <!-- Spacer for alignment -->
    </div>

    <!-- Main Content -->
    <div class="flex-1 overflow-y-auto p-6 text-center">
      <div class="bg-white rounded-2xl p-6 shadow-sm mb-6">
        <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-red-500" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <h2 class="text-xl font-bold text-gray-800 mb-2">Emergency Support</h2>
        <p class="text-gray-600 mb-6">If you're in immediate danger or need urgent help, please contact emergency
          services in your area.</p>

        <button
          class="w-full bg-red-500 hover:bg-red-600 text-white font-bold py-3 px-4 rounded-xl mb-4 flex items-center justify-center"
          @click="callEmergency">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
          </svg>
          Call Emergency Services (911)
        </button>
      </div>

      <div class="bg-white rounded-2xl p-6 shadow-sm mb-6 text-left">
        <h3 class="font-semibold text-gray-800 mb-3">Crisis Hotlines</h3>

        <div class="space-y-3">
          <div class="p-3 bg-blue-50 rounded-lg">
            <div class="font-medium">National Suicide Prevention Lifeline</div>
            <div class="text-blue-600">1-800-273-8255</div>
          </div>

          <div class="p-3 bg-blue-50 rounded-lg">
            <div class="font-medium">Crisis Text Line</div>
            <div class="text-blue-600">Text HOME to 741741</div>
          </div>

          <div class="p-3 bg-blue-50 rounded-lg">
            <div class="font-medium">Childhelp National Child Abuse Hotline</div>
            <div class="text-blue-600">1-800-422-4453</div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <h3 class="font-semibold text-gray-800 mb-3">Your Trusted Contacts</h3>

        <div class="space-y-3">
          <div v-for="contact in trustedContacts" :key="contact.id"
            class="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50">
            <div
              class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-semibold mr-3">
              {{ contact.name.charAt(0) }}
            </div>
            <div class="flex-1">
              <div class="font-medium">{{ contact.name }}</div>
              <div class="text-sm text-gray-500">{{ contact.relationship }}</div>
            </div>
            <a :href="'tel:' + contact.phone" class="text-blue-500 p-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const trustedContacts = ref([
  { id: 1, name: 'Mom', relationship: 'Parent', phone: '+1234567890' },
  { id: 2, name: 'Dad', relationship: 'Parent', phone: '+1234567891' },
  { id: 3, name: 'School Counselor', relationship: 'Counselor', phone: '+1234567892' },
]);

const callEmergency = () => {
  // In a real app, this would initiate a phone call to emergency services
  alert('Calling emergency services...');
};
</script>
