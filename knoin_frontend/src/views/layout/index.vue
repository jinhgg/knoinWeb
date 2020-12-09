<template>
  <div class="w">
    <nav-bar />
    <router-view />
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'

export default {
  components: { NavBar },
  name: 'Layout'
}
</script>

<style lang="less">
.bg-info {
  border-radius: 5px;
  .navbar-brand {
    margin: 0 0 0 10px !important;
  }
}
</style>
