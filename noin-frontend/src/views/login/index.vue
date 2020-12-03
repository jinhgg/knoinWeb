<template>

  <el-form ref="form" :model="form" label-width="80px">

    <el-form-item label="用户名">
      <el-input v-model="form.username"></el-input>
    </el-form-item>

    <el-form-item label="密码">
      <el-input v-model="form.password"></el-input>
    </el-form-item>

    <el-form-item>
      <el-checkbox v-model="form.checked">记住密码</el-checkbox>
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="onSubmit">登录</el-button>
    </el-form-item>
</el-form>
</template>
<script>
export default {
  name: 'Login',
  components: {},
  data () {
    return {
      form: {
        username: '',
        password: '',
        checked: true
      }
    }
  },
  created () {},
  methods: {
    onSubmit () {
      console.log('submit!')
    }
  }
}
</script>
<style lang="less" scoped>
.el-form {
  width: 400px;
  margin: 300px auto;
  padding: 50px;
  background-color: antiquewhite;
}
.el-form-item__content {
  margin: 0 auto;
}
</style>
