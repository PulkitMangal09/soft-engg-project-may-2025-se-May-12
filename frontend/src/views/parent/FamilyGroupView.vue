<template>
  <div class="bg-gray-100 font-sans p-4 md:p-6">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">👨‍👩‍👧‍👦 Smith Family Group</h1>
        <p class="text-sm text-gray-500">Family ID: SF_001234 • Created: January 2024</p>
      </div>
      <AppButton label="Edit" variant="secondary" size="sm" />
    </div>

    <!-- Join Requests -->
    <div class="mb-8">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold text-gray-700">🔔 Join Requests (2)</h2>
        <router-link to="#" class="text-sm font-medium text-blue-600 hover:underline">Manage All</router-link>
      </div>
      <div class="space-y-4">
        <AppCard v-for="request in joinRequests" :key="request.id">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
            <div class="flex items-center mb-4 sm:mb-0">
              <img :src="request.avatar" class="w-12 h-12 rounded-full mr-4 object-cover">
              <div>
                <p class="font-bold text-gray-800">{{ request.name }}</p>
                <p class="text-sm text-gray-500">{{ request.relationship }} • {{ request.time }}</p>
                <p class="text-sm text-gray-500">{{ request.email }}</p>
              </div>
            </div>
            <div class="flex flex-col space-y-2">
                <p class="text-sm bg-gray-100 p-2 rounded-md italic">"{{ request.message }}"</p>
                <div class="flex space-x-2 justify-end">
                    <AppButton label="✓ Approve" variant="success" size="sm" />
                    <AppButton label="✗ Reject" variant="error" size="sm" />
                    <AppButton label="👁 Profile" variant="secondary" size="sm" />
                </div>
            </div>
          </div>
        </AppCard>
      </div>
    </div>

    <!-- Family Members -->
    <div>
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold text-gray-700">👥 Family Members (5)</h2>
        <router-link to="#" class="text-sm font-medium text-blue-600 hover:underline">Manage</router-link>
      </div>
      <div class="bg-white rounded-lg shadow-sm">
        <ul class="divide-y divide-gray-200">
          <li v-for="member in familyMembers" :key="member.id" class="p-4 flex justify-between items-center">
            <div class="flex items-center">
              <span class="text-2xl mr-4">{{ member.icon }}</span>
              <div>
                <p class="font-semibold text-gray-800">{{ member.name }}</p>
                <p class="text-sm text-gray-500">{{ member.role }} • {{ member.status }}</p>
              </div>
            </div>
            <div class="flex space-x-2">
                <AppButton v-for="action in member.actions" :key="action.label" :label="action.label" :variant="action.variant" size="sm" />
            </div>
          </li>
        </ul>
      </div>
    </div>

  </div>
</template>

<script>
import { ref } from 'vue'
import AppCard from '@/components/ui/AppCard.vue'
import AppButton from '@/components/ui/AppButton.vue'

export default {
  name: 'FamilyGroupView',
  components: {
    AppCard,
    AppButton,
  },
  setup() {
    const joinRequests = ref([
      {
        id: 1,
        name: 'Alex Johnson',
        relationship: 'Nephew',
        time: '2 hours ago',
        email: 'alex.johnson@email.com',
        message: 'Hi Uncle John, please add me to family group for school project',
        avatar: 'https://randomuser.me/api/portraits/men/32.jpg',
      },
      {
        id: 2,
        name: 'Maria Smith',
        relationship: 'Daughter',
        time: '1 day ago',
        email: 'maria.smith@email.com',
        message: 'Dad, I need to join for my financial literacy class',
        avatar: 'https://randomuser.me/api/portraits/women/44.jpg',
      },
    ])

    const familyMembers = ref([
      { id: 1, icon: '👨', name: 'John Smith Sr. (You)', role: 'Moderator', status: 'Active', actions: [{label: '👑', variant: 'secondary'}] },
      { id: 2, icon: '👩', name: 'Sarah Smith', role: 'Moderator', status: 'Active', actions: [{label: '💬', variant: 'secondary'}, {label: '⚙', variant: 'secondary'}] },
      { id: 3, icon: '👦', name: 'John Smith Jr.', role: 'Child', status: 'Last active: 2 hours ago', actions: [{label: '📊', variant: 'secondary'}, {label: '✉', variant: 'secondary'}] },
      { id: 4, icon: '👧', name: 'Emma Smith', role: 'Child', status: 'Last active: 30 minutes ago', actions: [{label: '🚨', variant: 'error'}, {label: '📊', variant: 'secondary'}] },
      { id: 5, icon: '👶', name: 'Sophie Smith', role: 'Child', status: 'Last active: 1 hour ago', actions: [{label: '📊', variant: 'secondary'}, {label: '✉', variant: 'secondary'}] },
    ])

    return {
      joinRequests,
      familyMembers,
    }
  },
}
</script>
