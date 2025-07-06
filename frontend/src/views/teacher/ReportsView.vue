<template>
  <div class="p-6 md:p-8 bg-gray-100 min-h-screen">
    <!-- Header -->
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Student Reports</h1>
      <AppButton v-if="selectedStudent" label="Select Another Student" icon="🔄" @click="selectedStudent = null" variant="secondary" />
    </div>

    <!-- Student Selection -->
    <div v-if="!selectedStudent" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <h2 class="col-span-full text-xl font-semibold text-gray-700 mb-2">Please select a student to view their report:</h2>
        <div v-for="student in students" :key="student.id" @click="selectedStudent = student" 
             class="p-4 bg-white rounded-lg shadow-md flex items-center space-x-4 cursor-pointer hover:shadow-lg hover:-translate-y-1 transition-all">
            <img class="h-16 w-16 rounded-full object-cover" :src="student.avatar" :alt="student.name">
            <div>
                <p class="font-bold text-gray-800">{{ student.name }}</p>
                <p class="text-sm text-gray-500">Grade 9A</p>
            </div>
        </div>
    </div>

    <!-- Student Report -->
    <div v-else>
      <!-- Student Header -->
      <AppCard class="mb-8">
        <div class="flex flex-col md:flex-row items-start md:items-center justify-between">
            <div class="flex items-center mb-4 md:mb-0">
                <img class="h-20 w-20 rounded-full object-cover mr-6" :src="selectedStudent.avatar" :alt="selectedStudent.name">
                <div>
                    <h2 class="text-2xl font-bold text-gray-800">{{ selectedStudent.name }}</h2>
                    <p class="text-sm text-gray-500">Student ID: {{ selectedStudent.studentId }} • Grade 9A</p>
                    <AppBadge variant="error" class="mt-2">CRITICAL: Blood sugar 185 mg/dL (30 min ago) - Parent notified</AppBadge>
                </div>
            </div>
            <div class="grid grid-cols-3 gap-4 text-center w-full md:w-auto">
                <div><p class="text-3xl font-bold text-indigo-600">A</p><p class="text-xs text-gray-500">Overall Grade</p></div>
                <div><p class="text-3xl font-bold text-indigo-600">95%</p><p class="text-xs text-gray-500">Completion</p></div>
                <div><p class="text-3xl font-bold text-indigo-600">27/28</p><p class="text-xs text-gray-500">Tasks Done</p></div>
            </div>
        </div>
      </AppCard>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Left Column -->
        <div class="lg:col-span-2 space-y-8">
            <AppCard title="Health Summary" icon="🏥">
                <template #action><AppButton label="Details" size="sm" variant="secondary"/></template>
                <p class="font-semibold">Active Conditions:</p>
                <ul class="list-disc list-inside text-gray-700 mb-4">
                    <li>Type 1 Diabetes (Critical monitoring)</li>
                    <li>Nut allergy (Severe)</li>
                </ul>
                <p class="font-semibold">Current Status:</p>
                <ul class="list-disc list-inside text-gray-700">
                    <li>Blood sugar: 185 mg/dL <AppBadge variant="error">HIGH</AppBadge></li>
                    <li>Last medication: 6:00 PM ✓</li>
                    <li>Parent contact: Required immediately</li>
                </ul>
            </AppCard>
            <AppCard title="Academic Performance" icon="📈">
                <template #action><AppButton label="Full Report" size="sm" variant="secondary"/></template>
                <ul class="grid grid-cols-2 gap-4">
                    <li><span class="font-semibold">Task completion:</span> 96% (27/28)</li>
                    <li><span class="font-semibold">Average score:</span> 94%</li>
                    <li><span class="font-semibold">Improvement trend:</span> +8% this month</li>
                    <li><span class="font-semibold">Strong areas:</span> Financial literacy, Analytics</li>
                </ul>
            </AppCard>
        </div>
        <!-- Right Column -->
        <div class="space-y-8">
            <AppCard title="Recent Activity" icon="📋">
                <template #action><AppButton label="View All" size="sm" variant="secondary"/></template>
                <ul class="space-y-3 text-sm">
                    <li class="flex items-start"><span class="text-gray-500 w-24">Today 2:30 PM:</span><span class="flex-1">Completed budget analysis</span></li>
                    <li class="flex items-start"><span class="text-red-500 w-24">Today 1:45 PM:</span><span class="flex-1">High blood sugar alert</span></li>
                    <li class="flex items-start"><span class="text-gray-500 w-24">Yesterday:</span><span class="flex-1">Submitted financial goal project</span></li>
                    <li class="flex items-start"><span class="text-gray-500 w-24">2 days ago:</span><span class="flex-1">Perfect week achievement</span></li>
                </ul>
            </AppCard>
            <AppCard title="Actions">
                <div class="grid grid-cols-1 gap-3">
                    <AppButton label="Call Parent" icon="📞" variant="primary" />
                    <AppButton label="Assign Task" icon="📝" variant="secondary" />
                    <AppButton label="Full Report" icon="📊" variant="secondary" />
                </div>
            </AppCard>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import AppCard from '@/components/ui/AppCard.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppBadge from '@/components/ui/AppBadge.vue'

export default {
  name: 'ReportsView',
  components: { AppCard, AppButton, AppBadge },
  setup() {
    const selectedStudent = ref(null)
    const students = ref([
      {
        id: 1, name: 'Emma Smith', studentId: 'ES_2024_001', avatar: 'https://randomuser.me/api/portraits/women/68.jpg',
      },
      {
        id: 2, name: 'John Smith Jr.', studentId: 'JS_2024_002', avatar: 'https://randomuser.me/api/portraits/men/75.jpg',
      },
       {
        id: 3, name: 'Sarah Miller', studentId: 'SM_2024_003', avatar: 'https://randomuser.me/api/portraits/women/78.jpg',
      },
      {
        id: 4, name: 'Michael Rodriguez', studentId: 'MR_2024_004', avatar: 'https://randomuser.me/api/portraits/men/32.jpg',
      },
    ])
    
    // Pre-select a student for demonstration purposes
    selectedStudent.value = students.value[0];

    return { selectedStudent, students }
  }
}
</script>
