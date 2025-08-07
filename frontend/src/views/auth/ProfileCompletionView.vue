<template>
    <div class="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-md w-full space-y-8">
            <div class="text-center">
                <h2 class="text-3xl font-bold text-gray-900 mb-2">Complete Your Profile</h2>
                <p class="text-gray-600">Please provide some additional information to get started.</p>
            </div>

            <!-- Student Profile Form -->
            <form v-if="userType === 'student'" @submit.prevent="submitStudentProfile" class="space-y-6">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Student Number</label>
                    <input v-model="studentForm.student_number" type="text"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Enter student number" />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Grade Level</label>
                    <select v-model="studentForm.grade_level"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option value="">Select grade level</option>
                        <option value="9">Grade 9</option>
                        <option value="10">Grade 10</option>
                        <option value="11">Grade 11</option>
                        <option value="12">Grade 12</option>
                    </select>
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">School Name</label>
                    <input v-model="studentForm.school_name" type="text"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Enter school name" />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Emergency Contact Phone</label>
                    <input v-model="studentForm.emergency_contact_phone" type="tel"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Enter emergency contact phone" />
                </div>

                <div class="flex space-x-3">
                    <button type="button" @click="logout"
                        class="flex-1 px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50">
                        Cancel
                    </button>
                    <button type="submit" :disabled="loading"
                        class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50">
                        {{ loading ? 'Saving...' : 'Save Profile' }}
                    </button>
                </div>
            </form>

            <!-- Teacher Profile Form -->
            <form v-else-if="userType === 'teacher'" @submit.prevent="submitTeacherProfile" class="space-y-6">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">School Name *</label>
                    <input v-model="teacherForm.school_name" type="text" required
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Enter school name" />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">School District *</label>
                    <input v-model="teacherForm.school_district" type="text" required
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Enter school district" />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Subject/Grade</label>
                    <input v-model="teacherForm.subject_grade" type="text"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="e.g., Mathematics, Grade 10" />
                </div>

                <div class="flex space-x-3">
                    <button type="button" @click="logout"
                        class="flex-1 px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50">
                        Cancel
                    </button>
                    <button type="submit" :disabled="loading"
                        class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50">
                        {{ loading ? 'Saving...' : 'Save Profile' }}
                    </button>
                </div>
            </form>

            <!-- Parent Profile Form -->
            <form v-else-if="userType === 'parent'" @submit.prevent="submitParentProfile" class="space-y-6">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Full Name *</label>
                    <input v-model="parentForm.name" type="text" required
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Enter your full name" />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Family Group</label>
                    <input v-model="parentForm.group" type="text"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="e.g., Smith Family" />
                </div>

                <div class="flex items-center">
                    <input v-model="parentForm.is_head" type="checkbox" id="is_head"
                        class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" />
                    <label for="is_head" class="ml-2 block text-sm text-gray-700">
                        I am the head of the family
                    </label>
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
                    <textarea v-model="parentForm.description" rows="3"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Brief description about your role"></textarea>
                </div>

                <div class="flex space-x-3">
                    <button type="button" @click="logout"
                        class="flex-1 px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50">
                        Cancel
                    </button>
                    <button type="submit" :disabled="loading"
                        class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50">
                        {{ loading ? 'Saving...' : 'Save Profile' }}
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
    name: 'ProfileCompletionView',
    setup() {
        const store = useStore()
        const router = useRouter()
        const loading = ref(false)

        const userType = computed(() => store.getters['auth/userRole'])

        const studentForm = ref({
            student_number: '',
            grade_level: '',
            school_name: '',
            emergency_contact_phone: '',
            can_exist_independently: true
        })

        const teacherForm = ref({
            school_name: '',
            school_district: '',
            subject_grade: ''
        })

        const parentForm = ref({
            name: '',
            group: '',
            is_head: false,
            description: ''
        })

        const submitProfile = async () => {
            loading.value = true
            try {
                let profileData
                if (userType.value === 'student') {
                    profileData = studentForm.value
                } else if (userType.value === 'teacher') {
                    profileData = teacherForm.value
                } else if (userType.value === 'parent') {
                    profileData = parentForm.value
                }

                const result = await store.dispatch('auth/createProfile', profileData)

                if (result.success) {
                    // Profile completed, redirect to appropriate dashboard
                    router.push(`/${userType.value}`)
                } else {
                    console.error('Profile creation failed:', result.error)
                    // You could add toast notification here
                }
            } catch (error) {
                console.error('Error creating profile:', error)
                // You could add toast notification here
            } finally {
                loading.value = false
            }
        }

        const logout = () => {
            store.dispatch('auth/logout')
            router.push('/')
        }

        return {
            userType,
            loading,
            studentForm,
            teacherForm,
            parentForm,
            submitProfile,
            logout
        }
    }
}
</script>