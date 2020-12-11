<template>
  <b-breadcrumb>
    <b-breadcrumb-item href="/">
      <b-icon
        icon="house-fill"
        scale="1.25"
        shift-v="1.25"
        aria-hidden="true"
      ></b-icon>
      首页
    </b-breadcrumb-item>
    <b-breadcrumb-item
      v-for="bc in breadCrumb"
      :key="bc.href"
      :to="bc.href"
      :active="bc.isActive"
    >
      {{ bc.name }}
    </b-breadcrumb-item>
  </b-breadcrumb>
</template>

<script>
export default {
  name: 'BreadCrumb',
  props: {
    breadCrumb: {
      type: Array,
      default: () => []
    }
  }
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
