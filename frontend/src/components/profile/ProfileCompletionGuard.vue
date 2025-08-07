<template>
    <div>
        <slot v-if="!showProfileModal" />
        <ProfileCompletionModal v-else :user-type="userType" @close="handleClose"
            @profile-completed="handleProfileCompleted" />
    </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import ProfileCompletionModal from './ProfileCompletionModal.vue'

export default {
    name: 'ProfileCompletionGuard',
    components: {
        ProfileCompletionModal
    },
    setup() {
        const store = useStore()
        const router = useRouter()
        const checkingProfile = ref(false)

        const userType = computed(() => store.getters['auth/userRole'])
        const isAuthenticated = computed(() => store.getters['auth/isAuthenticated'])
        const hasProfile = computed(() => store.getters['auth/hasProfile'])

        const showProfileModal = computed(() => {
            return isAuthenticated.value && !hasProfile.value && !checkingProfile.value
        })

        const checkProfileStatus = async () => {
            if (!isAuthenticated.value) return

            checkingProfile.value = true
            try {
                await store.dispatch('auth/checkProfileStatus')
            } catch (error) {
                console.error('Error checking profile status:', error)
                // If there's an error, assume no profile exists
                store.commit('auth/SET_PROFILE_STATUS', { hasProfile: false, profileCompleted: false })
            } finally {
                checkingProfile.value = false
            }
        }

        const handleClose = () => {
            // If user cancels profile completion, log them out
            store.dispatch('auth/logout')
            router.push('/')
        }

        const handleProfileCompleted = () => {
            // Profile completed, user can now access the app
            checkProfileStatus()
        }

        onMounted(async () => {
            if (isAuthenticated.value) {
                await checkProfileStatus()
            }
        })

        return {
            userType,
            showProfileModal,
            handleClose,
            handleProfileCompleted
        }
    }
}
</script>