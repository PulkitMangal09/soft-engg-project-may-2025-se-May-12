<template>
  <div id="app">
    <ProfileCompletionGuard>
      <router-view />
    </ProfileCompletionGuard>
    <AppToast />
  </div>
</template>

<script>
import AppToast from '@/components/ui/AppToast.vue'
import ProfileCompletionGuard from '@/components/profile/ProfileCompletionGuard.vue'

export default {
  name: 'App',
  components: {
    AppToast,
    ProfileCompletionGuard
  }
}
</script>