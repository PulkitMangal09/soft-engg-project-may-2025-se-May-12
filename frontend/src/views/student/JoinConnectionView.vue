<template>
  <div class="min-h-screen bg-gray-50">
    <StudentNavBar />
    <div class="max-w-4xl mx-auto px-4 py-8">
      <!-- Header -->
      <div class="mb-8 text-center">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Join Connections</h1>
        <p class="text-lg text-gray-600">Connect with your teachers and parents using invitation codes</p>
      </div>

      <!-- Connection Status -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white rounded-xl shadow p-6 text-center">
          <span class="text-3xl mb-2">👨‍🏫</span>
          <div class="font-bold text-lg text-gray-800">{{ teacherConnections.length }}</div>
          <div class="text-sm text-gray-500">Teachers</div>
        </div>
        <div class="bg-white rounded-xl shadow p-6 text-center">
          <span class="text-3xl mb-2">👨‍👩‍👧‍👦</span>
          <div class="font-bold text-lg text-gray-800">{{ parentConnections.length }}</div>
          <div class="text-sm text-gray-500">Parents</div>
        </div>
        <div class="bg-white rounded-xl shadow p-6 text-center">
          <span class="text-3xl mb-2">⏳</span>
          <div class="font-bold text-lg text-gray-800">{{ pendingRequests.length }}</div>
          <div class="text-sm text-gray-500">Pending</div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Join Connection Form -->
        <div class="bg-white rounded-xl shadow p-6">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Enter Invitation Code</h2>
          
          <form @submit.prevent="joinConnection" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Invitation Code</label>
              <input 
                v-model="invitationCode" 
                type="text" 
                placeholder="e.g., MATH101-ABC123"
                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                required
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Message (Optional)</label>
              <textarea 
                v-model="message" 
                placeholder="Add a personal message..."
                rows="3"
                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              ></textarea>
            </div>

            <AppButton 
              type="submit" 
              label="Join Connection" 
              icon="🔗" 
              variant="primary" 
              :loading="isSubmitting"
              class="w-full"
            />
          </form>

          <div class="mt-6 p-4 bg-blue-50 rounded-lg">
            <h4 class="font-semibold text-blue-800 mb-2">How it works:</h4>
            <ul class="text-sm text-blue-700 space-y-1">
              <li>• Ask your teacher or parent for an invitation code</li>
              <li>• Enter the code above and send a request</li>
              <li>• They'll receive your request and can approve it</li>
              <li>• Once approved, you'll be connected!</li>
            </ul>
          </div>
        </div>

        <!-- Current Connections -->
        <div class="bg-white rounded-xl shadow p-6">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Your Connections</h2>
          
          <div v-if="allConnections.length === 0" class="text-center py-8">
            <span class="text-4xl mb-4 block">🔗</span>
            <p class="text-gray-500">No connections yet. Enter an invitation code to get started!</p>
          </div>

          <div v-else class="space-y-4">
            <!-- Teachers -->
            <div v-if="teacherConnections.length > 0">
              <h3 class="font-semibold text-gray-700 mb-3 flex items-center">
                <span class="text-xl mr-2">👨‍🏫</span>
                Teachers
              </h3>
              <div class="space-y-3">
                <div v-for="connection in teacherConnections" :key="connection.id" 
                     class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div class="flex items-center space-x-3">
                    <img :src="connection.avatar" class="h-10 w-10 rounded-full object-cover">
                    <div>
                      <p class="font-semibold text-gray-800">{{ connection.name }}</p>
                      <p class="text-sm text-gray-500">{{ connection.subject }}</p>
                    </div>
                  </div>
                  <AppBadge variant="success">Connected</AppBadge>
                </div>
              </div>
            </div>

            <!-- Parents -->
            <div v-if="parentConnections.length > 0">
              <h3 class="font-semibold text-gray-700 mb-3 flex items-center">
                <span class="text-xl mr-2">👨‍👩‍👧‍👦</span>
                Parents
              </h3>
              <div class="space-y-3">
                <div v-for="connection in parentConnections" :key="connection.id" 
                     class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div class="flex items-center space-x-3">
                    <img :src="connection.avatar" class="h-10 w-10 rounded-full object-cover">
                    <div>
                      <p class="font-semibold text-gray-800">{{ connection.name }}</p>
                      <p class="text-sm text-gray-500">{{ connection.relationship }}</p>
                    </div>
                  </div>
                  <AppBadge variant="success">Connected</AppBadge>
                </div>
              </div>
            </div>

            <!-- Pending Requests -->
            <div v-if="pendingRequests.length > 0">
              <h3 class="font-semibold text-gray-700 mb-3 flex items-center">
                <span class="text-xl mr-2">⏳</span>
                Pending Requests
              </h3>
              <div class="space-y-3">
                <div v-for="request in pendingRequests" :key="request.id" 
                     class="flex items-center justify-between p-3 bg-amber-50 rounded-lg">
                  <div class="flex items-center space-x-3">
                    <img :src="request.avatar" class="h-10 w-10 rounded-full object-cover">
                    <div>
                      <p class="font-semibold text-gray-800">{{ request.name }}</p>
                      <p class="text-sm text-gray-500">{{ request.type }}</p>
                    </div>
                  </div>
                  <AppBadge variant="warning">Pending</AppBadge>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="mt-8 bg-white rounded-xl shadow p-6">
        <h2 class="text-xl font-bold text-gray-800 mb-4">Recent Activity</h2>
        <div class="space-y-3">
          <div v-for="activity in recentActivity" :key="activity.id" 
               class="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
            <span class="text-lg">{{ activity.icon }}</span>
            <div class="flex-1">
              <p class="text-sm text-gray-800">{{ activity.message }}</p>
              <p class="text-xs text-gray-500">{{ activity.time }}</p>
            </div>
            <AppBadge :variant="activity.status === 'success' ? 'success' : 'warning'">
              {{ activity.status }}
            </AppBadge>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'
import StudentNavBar from '@/components/layout/StudentNavBar.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppBadge from '@/components/ui/AppBadge.vue'

export default {
  name: 'JoinConnectionView',
  components: { 
    StudentNavBar, 
    AppButton, 
    AppBadge 
  },
  setup() {
    const store = useStore()
    const invitationCode = ref('')
    const message = ref('')
    const isSubmitting = ref(false)

    // Mock data - in real app, this would come from API
    const teacherConnections = ref([
      {
        id: 1,
        name: 'Mrs. Johnson',
        subject: 'Mathematics',
        avatar: 'https://randomuser.me/api/portraits/women/44.jpg'
      },
      {
        id: 2,
        name: 'Mr. Smith',
        subject: 'Science',
        avatar: 'https://randomuser.me/api/portraits/men/32.jpg'
      }
    ])

    const parentConnections = ref([
      {
        id: 1,
        name: 'Mom',
        relationship: 'Mother',
        avatar: 'https://randomuser.me/api/portraits/women/68.jpg'
      },
      {
        id: 2,
        name: 'Dad',
        relationship: 'Father',
        avatar: 'https://randomuser.me/api/portraits/men/75.jpg'
      }
    ])

    const pendingRequests = ref([
      {
        id: 1,
        name: 'Mrs. Davis',
        type: 'English Teacher',
        avatar: 'https://randomuser.me/api/portraits/women/55.jpg'
      }
    ])

    const recentActivity = ref([
      {
        id: 1,
        icon: '✅',
        message: 'Connected with Mrs. Johnson (Mathematics)',
        time: '2 hours ago',
        status: 'success'
      },
      {
        id: 2,
        icon: '⏳',
        message: 'Request sent to Mrs. Davis (English)',
        time: '1 day ago',
        status: 'pending'
      },
      {
        id: 3,
        icon: '✅',
        message: 'Connected with Mom',
        time: '3 days ago',
        status: 'success'
      }
    ])

    const allConnections = ref([...teacherConnections.value, ...parentConnections.value])

    const joinConnection = async () => {
      if (!invitationCode.value.trim()) return

      isSubmitting.value = true

      try {
        // In real app, this would call the API
        await new Promise(resolve => setTimeout(resolve, 1000))

        // Simulate API call
        const newRequest = {
          id: Date.now(),
          name: 'New Connection',
          type: 'Teacher',
          avatar: 'https://randomuser.me/api/portraits/women/33.jpg'
        }

        pendingRequests.value.unshift(newRequest)

        // Add to recent activity
        recentActivity.value.unshift({
          id: Date.now(),
          icon: '⏳',
          message: `Request sent using code: ${invitationCode.value}`,
          time: 'Just now',
          status: 'pending'
        })

        store.dispatch('ui/showToast', {
          title: 'Request Sent!',
          message: 'Your connection request has been sent. You\'ll be notified when it\'s approved.',
          type: 'success',
        })

        // Reset form
        invitationCode.value = ''
        message.value = ''

      } catch (error) {
        store.dispatch('ui/showToast', {
          title: 'Error',
          message: 'Failed to send connection request. Please try again.',
          type: 'error',
        })
      } finally {
        isSubmitting.value = false
      }
    }

    return {
      invitationCode,
      message,
      isSubmitting,
      teacherConnections,
      parentConnections,
      pendingRequests,
      recentActivity,
      allConnections,
      joinConnection
    }
  }
}
</script>
