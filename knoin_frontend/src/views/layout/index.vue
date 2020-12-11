<template>
  <div class="w">
    <nav-bar />
    <router-view />
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'

export default {
  name: 'Layout',
  components: { NavBar }
}
</script>

<style lang="less">
.bg-info {
  border-radius: 5px;
}
</style>
