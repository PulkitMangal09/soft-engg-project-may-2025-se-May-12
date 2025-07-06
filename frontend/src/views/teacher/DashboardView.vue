<template>
    <div class="p-6 md:p-8 bg-gray-100 min-h-screen">
      <!-- Header -->
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Teacher's Dashboard</h1>
          <p class="text-lg text-gray-600 mt-1">Welcome back, Mrs. Johnson!</p>
        </div>
        <div class="mt-4 md:mt-0">
          <AppButton label="Assign New Task" icon="➕" variant="primary" />
        </div>
      </div>
  
      <!-- Key Metrics -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <AppCard icon="🎓" title="Class" subtitle="Grade 9A - Financial Literacy">
          <div class="text-right">
            <p class="text-3xl font-bold text-gray-800">28</p>
            <p class="text-sm text-gray-500">Students</p>
          </div>
        </AppCard>
        <AppCard icon="🔔" title="Health Alerts" variant="error">
           <div class="text-right">
            <p class="text-3xl font-bold text-red-500">2</p>
            <p class="text-sm text-gray-500">Urgent</p>
          </div>
        </AppCard>
        <AppCard icon="📝" title="Pending Tasks" variant="warning">
          <div class="text-right">
            <p class="text-3xl font-bold text-amber-500">15</p>
            <p class="text-sm text-gray-500">Awaiting Review</p>
          </div>
          <template #footer>
            <div class="flex justify-end">
              <router-link to="/teacher/tasks">
                <AppButton label="View All Tasks" variant="secondary" size="sm" />
              </router-link>
            </div>
          </template>
        </AppCard>
         <AppCard icon="📊" title="Class Average" variant="success">
          <div class="text-right">
            <p class="text-3xl font-bold text-emerald-500">B+</p>
            <p class="text-sm text-gray-500">Improving</p>
          </div>
        </AppCard>
      </div>
  
      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Left Column: Alerts and Students -->
        <div class="lg:col-span-2 space-y-8">
          <AppCard title="Urgent Health Alerts" icon="🚨" variant="error">
            <ul class="space-y-3">
              <li class="flex items-center justify-between">
                <div>
                  <p class="font-semibold text-gray-800">Emma S. - High Blood Sugar</p>
                  <p class="text-sm text-gray-500">185 mg/dL (30 min ago)</p>
                </div>
                <AppButton label="View Details" size="sm" variant="secondary" />
              </li>
               <li class="flex items-center justify-between">
                <div>
                  <p class="font-semibold text-gray-800">Leo M. - Asthma Action Plan</p>
                  <p class="text-sm text-gray-500">Reminder: Inhaler check needed</p>
                </div>
                <AppButton label="View Details" size="sm" variant="secondary" />
              </li>
            </ul>
          </AppCard>
  
          <AppCard title="Students Requiring Attention" icon="⚠️" variant="warning">
            <ul class="space-y-3">
              <li class="flex items-center justify-between">
                <div>
                  <p class="font-semibold text-gray-800">Michael R.</p>
                  <p class="text-sm text-gray-500">3 overdue assignments</p>
                </div>
                <AppButton label="View Student" size="sm" variant="secondary" />
              </li>
              <li class="flex items-center justify-between">
                <div>
                  <p class="font-semibold text-gray-800">Sophia T.</p>
                  <p class="text-sm text-gray-500">Falling behind in tasks</p>
                </div>
                <AppButton label="View Student" size="sm" variant="secondary" />
              </li>
               <li class="flex items-center justify-between">
                <div>
                  <p class="font-semibold text-gray-800">James L.</p>
                  <p class="text-sm text-gray-500">Low engagement this week</p>
                </div>
                <AppButton label="View Student" size="sm" variant="secondary" />
              </li>
            </ul>
             <template #footer>
              <div class="flex justify-end">
                <AppButton label="View All Students" variant="primary" />
              </div>
            </template>
          </AppCard>
        </div>
  
        <!-- Right Column: Achievements & Join Requests -->
        <div class="space-y-8">
          <AppCard title="Class Achievements" icon="✅" variant="success">
            <ul class="list-disc list-inside text-gray-700 space-y-2">
              <li>Sarah M.: Perfect task completion week</li>
              <li>David L.: Improved from C to A-</li>
              <li>Class: 90% attendance this week</li>
              <li>Overall: 15% improvement in grades</li>
            </ul>
            <template #footer>
              <div class="flex justify-end">
                  <AppButton label="Send Recognition" variant="secondary" />
              </div>
            </template>
          </AppCard>
  
          <AppCard title="Join Requests" icon="📧" @click="isJoinRequestsModalOpen = true" class="cursor-pointer hover:bg-gray-50 transition">
           <div class="flex items-center justify-between">
              <p class="text-lg font-semibold text-gray-700">{{ joinRequests.length }} new requests</p>
              <AppButton label="Review Requests" variant="primary" />
           </div>
        </AppCard>
        </div>
      </div>

      <AppModal :is-open="isJoinRequestsModalOpen" @close="isJoinRequestsModalOpen = false" title="Student Join Requests">
  <ul class="space-y-4">
    <li v-for="request in joinRequests" :key="request.id" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
        <div class="flex items-center space-x-4">
          <img :src="request.avatar" class="h-12 w-12 rounded-full object-cover">
          <p class="font-semibold text-gray-800">{{ request.name }}</p>
        </div>
        <div class="flex space-x-2">
          <AppButton label="Accept" variant="success" size="sm" @click="handleRequest(request.id, 'accepted')" />
          <AppButton label="Reject" variant="error" size="sm" @click="handleRequest(request.id, 'rejected')" />
        </div>
    </li>
  </ul>
  <div v-if="joinRequests.length === 0" class="text-center py-8">
      <p class="text-gray-500">No pending requests.</p>
  </div>
</AppModal>
    </div>
  </template>
  
  <script>
  // These components should be globally registered or imported locally
  import { ref } from 'vue'
import { useStore } from 'vuex'
import AppCard from '@/components/ui/AppCard.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppModal from '@/components/ui/AppModal.vue'
  
  export default {
    name: 'TeacherDashboard',
  components: {
    AppCard,
    AppButton,
    AppModal,
  },
    setup() {
    const store = useStore()
    const isJoinRequestsModalOpen = ref(false)
    const joinRequests = ref([
      { id: 1, name: 'Olivia Green', avatar: 'https://randomuser.me/api/portraits/women/33.jpg' },
      { id: 2, name: 'Ben Carter', avatar: 'https://randomuser.me/api/portraits/men/45.jpg' },
      { id: 3, name: 'Chloe Davis', avatar: 'https://randomuser.me/api/portraits/women/55.jpg' },
    ])

    const handleRequest = (id, status) => {
      const student = joinRequests.value.find(req => req.id === id)
      if (!student) return

      joinRequests.value = joinRequests.value.filter(req => req.id !== id)

      if (status === 'accepted') {
        store.dispatch('ui/showToast', {
          title: 'Request Accepted',
          message: `${student.name} has been added to your class.`,
          type: 'success',
        })
      } else {
        store.dispatch('ui/showToast', {
          title: 'Request Rejected',
          message: `${student.name}'s request has been rejected.`,
          type: 'error',
        })
      }
      
      if (joinRequests.value.length === 0) {
        isJoinRequestsModalOpen.value = false
      }
    }

    return {
      isJoinRequestsModalOpen,
      joinRequests,
      handleRequest,
    }
  },
  }
  </script>
  
  <style scoped>
  /* Scoped styles for the dashboard */
  </style>
  