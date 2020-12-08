<template>
  <div>
    <b-jumbotron>
      <template #header>传感染mNGS临床检测分析</template>

      <template #lead>
        （项目介绍）This is a simple hero unit, a simple jumbotron-style component for
        calling extra attention to featured content or information.
      </template>

      <hr class="my-4" />

      <p>
        It uses utility classes for typography and spacing to space content out
        within the larger container.
      </p>

      <b-button variant="success" href="#">进入使用</b-button>
      <b-button variant="primary" href="#">使用反馈</b-button>

    </b-jumbotron>
    <b-jumbotron>
      <template #header>肺癌小panel临床检测分析</template>

      <template #lead>
        （项目介绍）This is a simple hero unit, a simple jumbotron-style component for
        calling extra attention to featured content or information.
      </template>

      <hr class="my-4" />

      <p>
        It uses utility classes for typography and spacing to space content out
        within the larger container.
      </p>

      <b-button variant="success" href="#">进入使用</b-button>
      <b-button variant="primary" href="#">使用反馈</b-button>

    </b-jumbotron>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {

    }
  },
  methods: {

  }
}
</script>

<style lang="less" scoped>
.jumbotron {
  margin-bottom: 1rem;
  .btn {
    margin-right: 10px;
  }
}
</style>
