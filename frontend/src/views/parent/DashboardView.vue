<template>
  <div class="bg-gray-100 font-sans">
    <div class="p-4 md:p-6">
      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-2xl font-bold text-gray-800">Smith Family Group</h1>
        <p class="text-sm text-gray-500">Moderator: John Smith Sr.</p>
      </div>

      <!-- Key Metrics -->
      <div class="grid grid-cols-3 gap-4 mb-6 text-center">
        <div class="bg-white p-3 rounded-lg shadow-sm">
          <p class="text-2xl font-bold text-blue-600">3</p>
          <p class="text-xs text-gray-500">Children</p>
        </div>
        <div class="bg-white p-3 rounded-lg shadow-sm">
          <p class="text-2xl font-bold text-amber-500">2</p>
          <p class="text-xs text-gray-500">Pending Requests</p>
        </div>
        <div class="bg-white p-3 rounded-lg shadow-sm">
          <p class="text-2xl font-bold text-green-600">15</p>
          <p class="text-xs text-gray-500">Active Tasks</p>
        </div>
      </div>

      <!-- Children Selector -->
      <div class="flex items-center space-x-3 mb-6 overflow-x-auto pb-2">
        <button class="px-4 py-2 text-sm font-semibold text-white bg-blue-600 rounded-full shadow-md">All Children</button>
        <button v-for="child in children" :key="child.id" class="flex items-center space-x-2 px-4 py-2 text-sm font-semibold text-gray-700 bg-white rounded-full shadow-sm">
          <img :src="child.avatar" class="w-6 h-6 rounded-full object-cover">
          <span>{{ child.name }}</span>
        </button>
      </div>

      <!-- Urgent Alert -->
      <AppCard icon="🚨" title="Emma's blood sugar is elevated (180 mg/dL)" variant="error" class="mb-6">
        <p class="text-sm text-red-700">Immediate attention needed</p>
      </AppCard>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Attention Needed -->
        <AppCard title="⚠️ Attention Needed">
          <template #header-extra>
            <router-link to="/parent/tasks" class="text-sm font-medium text-blue-600 hover:underline">View All</router-link>
          </template>
          <ul class="space-y-3 text-sm text-gray-700">
            <li v-for="item in attentionItems" :key="item.text" class="flex items-start">
              <span class="mr-2">•</span>
              <span>{{ item.text }}</span>
            </li>
          </ul>
        </AppCard>

        <!-- Recent Achievements -->
        <AppCard title="✅ Recent Achievements">
          <template #header-extra>
            <AppButton label="Celebrate" size="sm" variant="secondary" />
          </template>
          <ul class="space-y-3 text-sm text-gray-700">
            <li v-for="item in achievements" :key="item.text">
              {{ item.text }}
            </li>
          </ul>
        </AppCard>
      </div>

      <!-- Quick Stats -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 text-center">
        <AppCard v-for="stat in quickStats" :key="stat.title" :icon="stat.icon" :title="stat.title" class="p-3">
          <p class="text-sm font-semibold text-gray-600">{{ stat.value }}</p>
        </AppCard>
      </div>

    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import AppCard from '@/components/ui/AppCard.vue'
import AppButton from '@/components/ui/AppButton.vue'

export default {
  name: 'ParentDashboard',
  components: {
    AppCard,
    AppButton,
  },
  setup() {
    const children = ref([
      { id: 1, name: 'John Jr.', avatar: 'https://randomuser.me/api/portraits/men/75.jpg' },
      { id: 2, name: 'Emma', avatar: 'https://randomuser.me/api/portraits/women/75.jpg' },
      { id: 3, name: 'Sophie', avatar: 'https://randomuser.me/api/portraits/women/76.jpg' },
    ])

    const attentionItems = ref([
      { text: 'John Jr.: Overdue math assignment' },
      { text: 'Emma: High sugar intake (3 days)' },
      { text: 'Sophie: Exceeded entertainment budget' },
    ])

    const achievements = ref([
      { text: 'John Jr.: Completed savings goal 🎮' },
      { text: 'Emma: 7-day water intake streak 💧' },
      { text: 'Sophie: Perfect task completion week ⭐' },
    ])

    const quickStats = ref([
        { icon: '📝', title: 'Tasks', value: '12 pending' },
        { icon: '💰', title: 'Finance', value: '2 goals active' },
        { icon: '🍎', title: 'Health', value: '1 alert' },
        { icon: '👥', title: 'Family', value: '2 requests' },
    ])

    return {
      children,
      attentionItems,
      achievements,
      quickStats,
    }
  },
}
</script>