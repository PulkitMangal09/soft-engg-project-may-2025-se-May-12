<template>
  <div class="p-6 md:p-8 bg-gray-100 min-h-screen">
    <!-- Header -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">My Students</h1>
        <p class="text-lg text-gray-600 mt-1">Grade 9A - Financial Literacy</p>
      </div>
      <div class="mt-4 md:mt-0">
        <AppButton label="Add New Student" icon="👤" variant="primary" />
      </div>
    </div>

    <!-- Filter Tabs -->
    <div class="mb-6 flex space-x-2 border-b border-gray-200">
      <button v-for="tab in tabs" :key="tab.name"
        @click="activeTab = tab.name"
        :class="['px-4 py-2 text-sm font-medium rounded-t-lg transition-colors duration-200',
                 activeTab === tab.name ? 'bg-white text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700']">
        {{ tab.name }} ({{ tab.count }})
      </button>
    </div>

    <!-- Student Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <AppCard v-for="student in students" :key="student.id" class="transform hover:-translate-y-1 transition-transform duration-200">
        <div class="flex flex-col items-center text-center">
          <div class="relative mb-4">
            <img class="h-24 w-24 rounded-full object-cover shadow-md" :src="student.avatar" :alt="student.name">
            <span class="absolute bottom-0 right-0 block h-6 w-6 rounded-full border-2 border-white"
                  :class="student.lastActive.includes('min') ? 'bg-green-400' : 'bg-gray-400'"></span>
          </div>
          <h3 class="text-lg font-bold text-gray-800">{{ student.name }}</h3>
          <p class="text-xs text-gray-500 mb-2">Last active: {{ student.lastActive }}</p>
          
          <AppBadge :variant="student.health.variant" class="mb-4">{{ student.health.text }}</AppBadge>

          <div class="w-full flex justify-around items-center border-t pt-3 mt-2">
            <div class="text-center">
              <p class="text-xl font-bold text-indigo-600">{{ student.grade }}</p>
              <p class="text-xs text-gray-500">Grade</p>
            </div>
            <div class="text-center">
              <p class="text-xl font-bold text-indigo-600">{{ student.completion }}%</p>
              <p class="text-xs text-gray-500">Tasks</p>
            </div>
          </div>
        </div>
      </AppCard>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import AppCard from '@/components/ui/AppCard.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppBadge from '@/components/ui/AppBadge.vue'

export default {
  name: 'MyStudentsView',
  components: { AppCard, AppButton, AppBadge },
  setup() {
    const activeTab = ref('All')
    const tabs = ref([
      { name: 'All', count: 28 },
      { name: 'Need Help', count: 5 },
      { name: 'Health Alerts', count: 2 },
      { name: 'Top Performers', count: 4 },
    ])

    const students = ref([
      {
        id: 1, name: 'Emma Smith', avatar: 'https://randomuser.me/api/portraits/women/68.jpg', lastActive: '30 min ago',
        health: { text: 'Diabetes - High blood sugar', variant: 'error' }, grade: 'A', completion: 95
      },
      {
        id: 2, name: 'John Smith Jr.', avatar: 'https://randomuser.me/api/portraits/men/75.jpg', lastActive: '2 hours ago',
        health: { text: 'No health conditions', variant: 'default' }, grade: 'A-', completion: 88
      },
      {
        id: 3, name: 'Sarah Miller', avatar: 'https://randomuser.me/api/portraits/women/78.jpg', lastActive: '45 min ago',
        health: { text: 'No health conditions', variant: 'default' }, grade: 'A+', completion: 98
      },
      {
        id: 4, name: 'Michael Rodriguez', avatar: 'https://randomuser.me/api/portraits/men/32.jpg', lastActive: '1 day ago',
        health: { text: 'ADHD - Medication tracking', variant: 'warning' }, grade: 'C-', completion: 65
      },
      {
        id: 5, name: 'Lisa Chen', avatar: 'https://randomuser.me/api/portraits/women/44.jpg', lastActive: '3 hours ago',
        health: { text: 'No health conditions', variant: 'default' }, grade: 'B+', completion: 82
      },
      {
        id: 6, name: 'David Thompson', avatar: 'https://randomuser.me/api/portraits/men/11.jpg', lastActive: '6 hours ago',
        health: { text: 'No health conditions', variant: 'default' }, grade: 'B', completion: 79
      },
    ])

    return { activeTab, tabs, students }
  }
}
</script>
