<template>
  <div>
    <b-card class="login-form" header="南京诺因生物—临床检测分析报告系统">
      <b-form @submit="onSubmit" @reset="onReset" v-if="show">
        <b-form-group id="input-group-1" label="用户名:" label-for="input-1">
          <b-form-input
            id="input-1"
            v-model="loginForm.username"
            type="text"
            :state="validation"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-2" label="密码:" label-for="input-2">
          <b-form-input
            id="input-2"
            v-model="loginForm.password"
            type="password"
            :state="validation"
            required
          ></b-form-input>
          <b-form-invalid-feedback :state="validation">
            用户名或密码错误！
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group id="input-group-3">
          <b-form-checkbox-group v-model="loginForm.checked" id="checkboxes-3">
            <b-form-checkbox>记住密码</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <div class="button-group">
          <b-button type="submit" variant="primary">登录</b-button>
          <b-button type="reset" variant="danger">重置</b-button>
        </div>
      </b-form>
      <!-- <b-card class="mt-3" header="Form Data Result">
        <pre class="m-0">{{ loginForm }}</pre>
      </b-card> -->
        <b-link href="#foo">注册</b-link> |
        <b-link href="#foo">忘记密码</b-link>
    </b-card>
  </div>
</template>

<script>
import { login } from '@/api/user'

export default {
  data() {
    return {
      loginForm: {
        username: '',
        password: '',
        checked: ['true']
      },
      validation: null,
      show: true
    }
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault()
      // alert(JSON.stringify(this.loginForm))
      login(this.loginForm).then(res => {
        console.log('登录成功！')
      }).catch(err => {
        this.validation = false
        console.log('xxx', err)
      })
    },
    onReset(evt) {
      evt.preventDefault()
      this.loginForm.username = ''
      this.loginForm.password = ''
      this.loginForm.checked = true
      this.validation = null
      this.show = false
      this.$nextTick(() => {
        this.show = true
      })
    }
  }
}
</script>

<style lang="less" scoped>
.login-form {
  width: 500px;
  margin: 200px auto;
}
.button-group {
  text-align: center;
  .btn-primary {
    margin: 0 10px;
  }
}
</style>
