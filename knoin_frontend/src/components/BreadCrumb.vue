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
.breadcrumb {
  background-color: #fff !important;
  margin-top: 1rem;
  margin-bottom: 1rem;
}
</style>
