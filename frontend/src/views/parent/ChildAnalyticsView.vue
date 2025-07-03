<template>
  <div class="bg-gray-100 font-sans p-4 md:p-6">
    <!-- Header -->
    <div class="flex items-center mb-6">
        <img :src="child.avatar" class="w-16 h-16 rounded-full mr-4 object-cover border-4 border-white shadow-lg">
        <div>
            <h1 class="text-2xl font-bold text-gray-800">{{ child.name }}'s Analytics 📊</h1>
        </div>
    </div>

    <!-- Overall Performance -->
    <AppCard title="📈 Overall Performance" class="mb-6">
        <template #header-extra>
            <span class="text-sm font-medium text-gray-500">This Month</span>
        </template>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div v-for="metric in overallMetrics" :key="metric.label" class="bg-gray-50 p-3 rounded-lg">
                <p class="text-xl font-bold text-gray-800">{{ metric.value }}</p>
                <p class="text-xs text-gray-500">{{ metric.label }}</p>
            </div>
        </div>
        <ul class="mt-4 text-sm text-gray-600 space-y-1">
            <li>Tasks: 85% completion rate ⬆️</li>
            <li>Finance: On track with 2/3 goals 💰</li>
            <li>Health: Good dietary habits ✅</li>
            <li>Mood: Stable emotional patterns 😊</li>
        </ul>
    </AppCard>

    <!-- Detailed Sections -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Task Performance -->
        <AppCard title="📝 Task Performance">
            <template #header-extra>
                <router-link :to="{ name: 'ParentTasks' }" class="text-sm font-medium text-blue-600 hover:underline">Details</router-link>
            </template>
            <div class="h-48 mb-4">
                <Line :data="taskChartData" :options="chartOptions" />
            </div>
            <ul class="text-sm text-gray-600 space-y-1">
                <li>Best day: Friday (100%)</li>
                <li>Most challenging: Monday (60%)</li>
                <li>Favorite category: Creative tasks</li>
            </ul>
        </AppCard>

        <!-- Financial Habits -->
        <AppCard title="💰 Financial Habits">
            <template #header-extra>
                <router-link to="#" class="text-sm font-medium text-blue-600 hover:underline">Details</router-link>
            </template>
             <div class="h-48 mb-4">
                <Bar :data="financeChartData" :options="chartOptions" />
            </div>
            <ul class="text-sm text-gray-600 space-y-1">
                <li>Savings rate: 25% (Excellent!)</li>
                <li>Top spending: Entertainment (40%)</li>
                <li>Goal progress: Gaming console 62%</li>
            </ul>
        </AppCard>

        <!-- Health & Nutrition -->
        <AppCard title="🍎 Health & Nutrition">
             <template #header-extra>
                <router-link to="#" class="text-sm font-medium text-blue-600 hover:underline">Details</router-link>
            </template>
            <div class="space-y-4">
                <div class="flex items-center justify-between">
                    <span class="font-medium">Water Intake</span>
                    <span class="font-bold text-green-600">7/8 glasses daily ⭐</span>
                </div>
                <div class="flex items-center justify-between">
                    <span class="font-medium">Balanced Meals</span>
                    <span class="font-bold">85% of days</span>
                </div>
                 <div class="flex items-center justify-between">
                    <span class="font-medium">Exercise</span>
                    <span class="font-bold">4 days/week average</span>
                </div>
                 <div class="flex items-center justify-between">
                    <span class="font-medium">Sleep</span>
                    <span class="font-bold">8.5 hours average</span>
                </div>
            </div>
        </AppCard>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import AppCard from '@/components/ui/AppCard.vue'
import { Line, Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, BarElement, CategoryScale, LinearScale, PointElement)

export default {
  name: 'ParentChildAnalyticsView',
  components: {
    AppCard,
    Line,
    Bar
  },
  props: {
      childId: {
          type: String,
          required: true
      }
  },
  setup(props) {
    const children = {
        '1': { id: 1, name: 'John Jr.', avatar: 'https://randomuser.me/api/portraits/men/75.jpg' },
        '2': { id: 2, name: 'Emma', avatar: 'https://randomuser.me/api/portraits/women/75.jpg' },
        '3': { id: 3, name: 'Sophie', avatar: 'https://randomuser.me/api/portraits/women/76.jpg' },
    }

    const child = computed(() => children[props.childId] || { name: 'Child', avatar: '' })

    const overallMetrics = ref([
      { label: 'Tasks Completed', value: '23/27' },
      { label: 'Current Balance', value: '$247.50' },
      { label: 'BMI (Normal)', value: '22.6' },
      { label: 'Avg Mood Score', value: '7.5/10' },
    ])

    const taskChartData = ref({
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      datasets: [
        {
          label: 'Task Completion',
          backgroundColor: '#3b82f6',
          borderColor: '#3b82f6',
          data: [60, 75, 80, 85, 100, 90, 95],
          tension: 0.4,
        },
      ],
    })

    const financeChartData = ref({
        labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        datasets: [
            {
                label: 'Spending',
                backgroundColor: '#ef4444',
                data: [50, 60, 55, 70]
            },
            {
                label: 'Saving',
                backgroundColor: '#22c55e',
                data: [20, 25, 30, 35]
            }
        ]
    })

    const chartOptions = ref({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
      },
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    })

    return {
      child,
      overallMetrics,
      taskChartData,
      financeChartData,
      chartOptions,
    }
  },
}
</script>
