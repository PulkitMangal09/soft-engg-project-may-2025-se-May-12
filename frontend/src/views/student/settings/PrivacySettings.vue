<template>
  <div class="p-4 max-w-3xl mx-auto">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-800 mb-2">Privacy Settings</h1>
      <p class="text-gray-600">Control who can see your information and how it's used</p>
    </div>

    <!-- Privacy Card -->
    <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
      <h2 class="text-lg font-semibold text-gray-700 mb-6">Data Privacy</h2>
      
      <!-- Data Collection Toggle -->
      <div class="flex items-center justify-between py-4 border-b border-gray-100">
        <div>
          <h3 class="font-medium text-gray-800">Data Collection</h3>
          <p class="text-sm text-gray-500">Allow anonymous data collection to help improve our services</p>
        </div>
        <label class="relative inline-flex items-center cursor-pointer">
          <input type="checkbox" v-model="dataCollection" class="sr-only peer">
          <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
        </label>
      </div>

      <!-- Activity Sharing -->
      <div class="flex items-center justify-between py-4 border-b border-gray-100">
        <div>
          <h3 class="font-medium text-gray-800">Share Activity with Counselors</h3>
          <p class="text-sm text-gray-500">Allow school counselors to view your mood and activity data</p>
        </div>
        <label class="relative inline-flex items-center cursor-pointer">
          <input type="checkbox" v-model="shareWithCounselors" class="sr-only peer">
          <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
        </label>
      </div>

      <!-- Emergency Access -->
      <div class="flex items-center justify-between py-4 border-b border-gray-100">
        <div>
          <h3 class="font-medium text-gray-800">Emergency Access</h3>
          <p class="text-sm text-gray-500">Allow trusted contacts to be notified in case of emergency</p>
        </div>
        <label class="relative inline-flex items-center cursor-pointer">
          <input type="checkbox" v-model="emergencyAccess" class="sr-only peer">
          <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
        </label>
      </div>
    </div>

    <!-- Account Privacy -->
    <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
      <h2 class="text-lg font-semibold text-gray-700 mb-6">Account Privacy</h2>
      
      <!-- Profile Visibility -->
      <div class="mb-6">
        <h3 class="font-medium text-gray-800 mb-2">Profile Visibility</h3>
        <p class="text-sm text-gray-500 mb-3">Who can see your profile information</p>
        <div class="space-y-2">
          <div v-for="option in visibilityOptions" :key="option.value" class="flex items-center">
            <input 
              :id="option.value" 
              v-model="profileVisibility" 
              :value="option.value" 
              type="radio" 
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
            >
            <label :for="option.value" class="ml-3 block text-sm font-medium text-gray-700">
              {{ option.label }}
            </label>
          </div>
        </div>
      </div>

      <!-- Data Export -->
      <div class="pt-4 border-t border-gray-100">
        <h3 class="font-medium text-gray-800 mb-3">Your Data</h3>
        <button 
          @click="exportData"
          class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <svg class="-ml-1 mr-2 h-5 w-5 text-gray-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
          Export My Data
        </button>
        <p class="mt-2 text-xs text-gray-500">Download a copy of all your data in a machine-readable format</p>
      </div>
    </div>

    <!-- Privacy Notice -->
    <div class="bg-blue-50 rounded-xl p-6">
      <h2 class="text-lg font-semibold text-blue-800 mb-2">Your Privacy Matters</h2>
      <p class="text-blue-700 text-sm mb-4">
        We take your privacy seriously. Your emotional data is encrypted and stored securely. 
        We never sell your personal information to third parties.
      </p>
      <a href="#" class="text-blue-600 hover:text-blue-800 text-sm font-medium">
        Learn more about our privacy policy →
      </a>
    </div>

    <!-- Save Button -->
    <div class="mt-8">
      <button 
        @click="saveSettings"
        class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition duration-150 ease-in-out"
      >
        Save Changes
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import 'vue-toastification/dist/index.css';

const router = useRouter();
const toast = useToast();

// Load saved settings from localStorage
const loadSettings = () => {
  const savedSettings = localStorage.getItem('privacySettings');
  if (savedSettings) {
    const parsed = JSON.parse(savedSettings);
    dataCollection.value = parsed.dataCollection ?? true;
    shareWithCounselors.value = parsed.shareWithCounselors ?? false;
    emergencyAccess.value = parsed.emergencyAccess ?? false;
    profileVisibility.value = parsed.profileVisibility ?? 'private';
  }
};

// Save settings to localStorage
const saveSettings = () => {
  const settings = {
    dataCollection: dataCollection.value,
    shareWithCounselors: shareWithCounselors.value,
    emergencyAccess: emergencyAccess.value,
    profileVisibility: profileVisibility.value
  };
  
  localStorage.setItem('privacySettings', JSON.stringify(settings));
  toast.success('Settings saved successfully');
};

// Export user data
const exportData = () => {
  const data = {
    // Add actual data to export here
    lastUpdated: new Date().toISOString(),
    settings: {
      dataCollection: dataCollection.value,
      shareWithCounselors: shareWithCounselors.value,
      emergencyAccess: emergencyAccess.value,
      profileVisibility: profileVisibility.value
    }
  };
  
  const dataStr = JSON.stringify(data, null, 2);
  const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
  
  const exportFileDefaultName = `user-data-${new Date().toISOString().split('T')[0]}.json`;
  
  const linkElement = document.createElement('a');
  linkElement.setAttribute('href', dataUri);
  linkElement.setAttribute('download', exportFileDefaultName);
  linkElement.click();
  
  toast.info('Data exported successfully');
};

// Privacy settings state
const dataCollection = ref(true);
const shareWithCounselors = ref(false);
const emergencyAccess = ref(true);
const profileVisibility = ref('private');

const visibilityOptions = [
  { value: 'public', label: 'Public - Anyone can see your profile' },
  { value: 'friends', label: 'Friends - Only your friends can see your profile' },
  { value: 'private', label: 'Private - Only you can see your profile' },
];

// Initialize
loadSettings();
</script>

<style scoped>
/* Custom styles for the toggle switch */
input[type="checkbox"]:checked + div {
  background-color: #2563eb; /* bg-blue-600 */
}
</style>
