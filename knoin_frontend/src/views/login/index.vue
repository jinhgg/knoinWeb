<template>
  <div>
    <b-card class="login-form" header="南京诺因生物—临床检测分析报告系统">
      <b-form @submit="onSubmit" @reset="onReset" v-if="show">
        <b-form-group id="input-group-1" label="用户名:" label-for="input-1">
          <b-form-input
            id="input-1"
            v-model="loginForm.username"
            type="text"
            :state="validForm.username.isValid"
            required
          ></b-form-input>
          <b-form-invalid-feedback>
            {{ validForm.username.info }}
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group id="input-group-2" label="密码:" label-for="input-2">
          <b-form-input
            id="input-2"
            v-model="loginForm.password"
            type="password"
            :state="validForm.password.isValid"
            required
          ></b-form-input>
          <b-form-invalid-feedback>
            {{ validForm.password.info }}
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group id="input-group-3">
          <b-form-checkbox-group v-model="loginForm.checked" id="checkboxes-3">
            <b-form-checkbox>记住密码</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <div class="button-group">
          <!-- <router-link to="/"> -->
            <!-- <b-button variant="primary">登录</b-button> -->
            <b-button type="submit" variant="primary">登录</b-button>

          <!-- </router-link> -->
          <b-button type="reset" variant="danger">重置</b-button>
        </div>
      </b-form>
      <!-- <b-card class="mt-3" header="Form Data Result">
        <pre class="m-0">{{ loginForm }}</pre>
      </b-card> -->
      <b-link href="/#/register">注册</b-link> |
      <b-link href="#foo">忘记密码</b-link>
    </b-card>
  </div>
</template>

<script>
import { login } from '@/api/user'
export default {
  name: 'Login',
  created() {
  },
  data() {
    return {
      loginForm: {
        username: window.localStorage.getItem('username'),
        password: window.atob(window.localStorage.getItem('password') || ''),
        checked: [true]
      },
      validForm: {
        username: { isValid: null, info: '' },
        password: { isValid: null, info: '' }
      },
      show: true
    }
  },
  methods: {
    checkForm() {
      const loginForm = this.loginForm
      const vaildForm = this.validForm
      let vaild = true
      if (loginForm.username.length < 3 || loginForm.username.length > 50) {
        vaildForm.username = { isValid: false, info: '用户名应在3~50位之间' }
        vaild = false
      }
      if (loginForm.password.length < 3) {
        vaildForm.password = { isValid: false, info: '密码长度不能小于3位' }
        vaild = false
      }
      return vaild
    },
    showErrMsg(msg) {
      this.resetValidForm()
      this.validForm = {
        username: { isValid: false, info: '' },
        password: { isValid: false, info: '用户名或密码错误' }
      }
    },
    resetValidForm() {
      this.validForm = {
        username: { isValid: null, info: '' },
        password: { isValid: null, info: '' }
      }
    },
    onSubmit(evt) {
      evt.preventDefault()
      this.resetValidForm()
      if (this.checkForm() === false) { return }
      // alert(JSON.stringify(this.loginForm))
      login(this.loginForm).then(res => {
        if (this.loginForm.checked[0] === true) {
          window.localStorage.setItem('username', this.loginForm.username)
          window.localStorage.setItem('password', window.btoa(this.loginForm.password))
        } else {
          window.localStorage.removeItem('username')
          window.localStorage.removeItem('password')
        }
        window.localStorage.setItem('userId', res.data.id)
        this.$router.push({ name: 'Home' })
      }).catch(err => {
        if (err.response === undefined) {
          alert('服务器停止运行')
        }
        this.showErrMsg(err.response.data)
      })
    },
    onReset(evt) {
      evt.preventDefault()
      this.loginForm.username = ''
      this.loginForm.password = ''
      this.loginForm.checked = [true]
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
}
</style>
