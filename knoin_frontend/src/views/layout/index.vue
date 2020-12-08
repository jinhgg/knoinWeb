<template>
  <div class="w">
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand href="#"
        >南京诺因生物—临床检测分析报告系统</b-navbar-brand
      >
      <b-navbar-nav class="mr-auto"> </b-navbar-nav>
      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item href="#">FAQ | 帮助</b-nav-item>
        <b-nav-item href="#">文件上传</b-nav-item>
        <b-navbar-brand href="#">
          <img src="https://placekitten.com/g/30/30" alt="Kitten" />
        </b-navbar-brand>
        <b-nav-item-dropdown text="Lijinhang" right>
          <b-dropdown-item href="#">个人中心</b-dropdown-item>
          <b-dropdown-item href="#">退出登录</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-navbar>
    <router-view />
  </div>
</template>

<style lang="less">
.bg-info {
  border-radius: 5px;
  .navbar-brand {
    margin: 0 0 0 10px !important;
  }
}
</style>
