<template>
  <div>
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
      <b-breadcrumb-item href="#" active
        >肺癌小panel临床检测分析</b-breadcrumb-item
      >
    </b-breadcrumb>

    <b-card title="Card Title" no-body>
      <b-card-header header-tag="nav">
        <b-nav card-header pills>
          <b-nav-item :active="curNav == 0" @click="curNav = 0"
            >新建项目</b-nav-item
          >
          <b-nav-item :active="curNav == 1" @click="curNav = 1"
            >进行中</b-nav-item
          >
          <b-nav-item :active="curNav == 2" @click="curNav = 2"
            >已完成</b-nav-item
          >
        </b-nav>
      </b-card-header>

      <b-card-body v-show="curNav == 0" class="text-center">
        <b-card-text> 000000000000000000000000000 </b-card-text>
        <b-button variant="primary">Go somewhere</b-button>
      </b-card-body>
      <b-card-body v-show="curNav == 1" class="text-center">
        <b-card-text> 1111111111111111111111111111111 </b-card-text>
        <b-button variant="primary">Go somewhere</b-button>
      </b-card-body>
      <b-card-body v-show="curNav == 2" class="text-center">
        <b-card-text> 222222222222222222222222222 </b-card-text>
        <b-button variant="primary">Go somewhere</b-button>
      </b-card-body>
    </b-card>
  </div>
</template>

<script>
export default {
  name: 'Project02',
  data() {
    return {
      curNav: 0
    }
  }
}
</script>

<style lang="less" scoped>
.breadcrumb {
  background-color: #fff;
  margin-top: 1rem;
  margin-bottom: 1rem;
}
.nav-link.active {
  background-color: #3590F3 !important;
}
</style>
