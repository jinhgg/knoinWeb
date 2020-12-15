<template>
  <div>
    <bread-crumb :breadCrumb="breadCrumb" />
    <b-card>
      <h3>测序数据</h3>
      <b-form-file v-model="file01" ref="file-input" class="mb-2"></b-form-file>

      <h3>参考数据</h3>
      <b-form-file v-model="file02" ref="file-input" class="mb-2"></b-form-file>

      <h3>区域文件</h3>
      <b-form-file v-model="file03" ref="file-input" class="mb-2"></b-form-file>
      <div class="button-upload">
        <b-button variant="primary">上传</b-button>
        <b-button variant="danger">重置</b-button>
      </div>
    </b-card>
    <div class="desc">
      <h3>格式描述</h3>
    </div>
  </div>
</template>

<script>
import BreadCrumb from '@/components/BreadCrumb.vue'

export default {
  name: 'Upload',
  components: { BreadCrumb },
  data() {
    return {
      breadCrumb: [{ href: '', name: '文件上传', isActive: true }],
      file01: null,
      file02: null,
      file03: null
    }
  }
}
</script>

<style lang="less" scoped>
.card {
  width: 40%;
  float: left;
}
.desc {
  width: 40%;
  float: left;
  margin: 0 150px;
}
.button-upload {
  text-align: center;
  button {
    width: 100px;
    margin-top: 15px;
  }
}
</style>
