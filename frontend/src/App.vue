<template>
  <div id="app">
    <router-view />
    <AppToast />
  </div>
</template>

<script>
import AppToast from '@/components/ui/AppToast.vue';

export default {
  name: 'App',
  components: {
    AppToast
  }
}
</script>