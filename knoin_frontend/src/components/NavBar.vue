<template>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand :to="{ name: 'Home' }">
        <img class="logo" src="../assets/logo.png">
        南京诺因生物—临床检测分析报告系统
      </b-navbar-brand>
      <b-navbar-nav class="mr-auto"> </b-navbar-nav>
      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item :to="{ name: 'Help' }">FAQ | 帮助</b-nav-item>
        <b-nav-item :to="{ name: 'Upload' }">文件上传</b-nav-item>
          <b-avatar class="avatar"></b-avatar>
        <b-nav-item-dropdown text="Admin" right>
          <b-dropdown-item href="#">个人中心</b-dropdown-item>
          <b-dropdown-item href="#">退出登录</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-navbar>
    <!-- <router-view /> -->
</template>

<script>
export default {
  name: 'NavBar'
}
</script>

<style lang="less">
.bg-info {
  border-radius: 5px;
  .logo {
    width: 55px;
    vertical-align: bottom;
  }
  .avatar {
    width: 30px;
    height: 30px;
    margin: auto;
    margin-left: 8px;
  }
}
</style>
