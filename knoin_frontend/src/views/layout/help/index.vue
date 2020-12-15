<template>
  <div>
    <bread-crumb :breadCrumb="breadCrumb" />
    <b-card header="FAQ">
      <b-media>
        <template #aside>
          <b-avatar></b-avatar>
        </template>
        <h5 class="mt-0">匿名用户</h5>
        <p>
          Cras sit amet nibh libero, in gravida nulla. Nulla vel metus
          scelerisque ante sollicitudin. Cras purus odio, vestibulum in
          vulputate at, tempus viverra turpis. Fusce condimentum nunc ac nisi
          vulputate fringilla. Donec lacinia congue felis in faucibus.
        </p>
        <b-media>
          <template #aside>
            <b-avatar></b-avatar>
          </template>
          <h5 class="mt-0">管理员</h5>
          <p class="mb-0">
            Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia
            congue felis in faucibus.
          </p>
        </b-media>
      </b-media>
      <div class="upQuestion">
        <b-button v-b-toggle.collapse-1 variant="primary" size="sm"
          >发表问题</b-button
        >
        <b-collapse id="collapse-1" class="mt-2">
            <b-form-textarea
              id="textarea-no-resize"
              placeholder="问题描述"
              rows="3"
              no-resize
            ></b-form-textarea>
            <b-button class="submit" size="sm" left>提交</b-button>
        </b-collapse>
      </div>
    </b-card>
    <div class="downDocument">
      <b-button variant="outline-success">使用文档下载</b-button>
    </div>
  </div>
</template>

<script>
import BreadCrumb from '@/components/BreadCrumb.vue'

export default {
  name: 'Help',
  components: { BreadCrumb },
  data() {
    return {
      breadCrumb: [
        { href: '', name: '使用帮助', isActive: true }
      ]
    }
  }
}
</script>

<style lang="less" scoped>
.card {
  width: 45%;
  float: left;
  .downDocument {
    text-align: center;
  }
  .upQuestion {
    margin-top: 20px;
    text-align: center;
    .submit {
    float: right;
    margin: 0;
}
  }
}
</style>
