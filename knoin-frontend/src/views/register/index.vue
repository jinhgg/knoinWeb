<template>
  <div>
    <b-card class="register-form" header="南京诺因生物—临床检测分析报告系统">
      <b-form @submit="onSubmit" @reset="onReset" v-if="show">
        <b-form-group id="input-group-1" label="用户名:" label-for="input-1">
          <b-form-input
            id="input-1"
            v-model="registerForm.username"
            type="text"
            :state="validation.username.isValid"
            required
          ></b-form-input>
          <b-form-invalid-feedback :state="validation.username.isValid">
            {{validation.username.info}}
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group id="input-group-2" label="密码:" label-for="input-2">
          <b-form-input
            id="input-2"
            v-model="registerForm.password"
            type="password"
            :state="validation.password.isValid"
            required
          ></b-form-input>
          <b-form-invalid-feedback :state="validation.password.isValid">
            {{validation.password.info}}
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group id="input-group-3" label="重复密码:" label-for="input-3">
          <b-form-input
            id="input-3"
            v-model="registerForm.repassword"
            type="password"
            :state="validation.repassword.isValid"
            required
          ></b-form-input>
          <b-form-invalid-feedback :state="validation.repassword.isValid">
            {{validation.repassword.info}}
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group id="input-group-4" label="手机号:" label-for="input-4">
          <b-form-input
            id="input-4"
            v-model="registerForm.moblie"
            type="tel"
            :state="validation.mobile.isValid"
            required
          ></b-form-input>
          <b-form-invalid-feedback :state="validation.mobile.isValid">
            {{validation.mobile.info}}
          </b-form-invalid-feedback>
        </b-form-group>
        <div class="button-group">
          <b-button type="submit" variant="primary">注册</b-button>
          <b-button type="reset" variant="danger">重置</b-button>
        </div>
      </b-form>
      <b-card class="mt-3" header="Form Data Result">
        <pre class="m-0">{{ registerForm }}</pre>
      </b-card>
    </b-card>
  </div>
</template>

<script>
import { register, checkRegister } from '@/api/user'

export default {
  name: 'Register',
  data() {
    return {
      registerForm: {
        username: '',
        password: '',
        repassword: '',
        moblie: ''
      },
      validation: {
        username: { isValid: null, info: '' },
        password: { isValid: null, info: '' },
        repassword: { isValid: null, info: '' },
        mobile: { isValid: null, info: '' }
      },
      show: true
    }
  },
  methods: {
    checkForm() {
      this.validation = checkRegister(this.registerForm)
      return false
    },
    onSubmit(evt) {
      evt.preventDefault()
      if (this.checkForm() === false) {
        return
      }
      // alert(JSON.stringify(this.loginForm))
      register(this.registerForm).then(res => {
        console.log('注冊成功！')
      }).catch(err => {
        this.usernameValidation = false
        console.log('xxx', err)
      })
    },
    onReset(evt) {
      evt.preventDefault()
      this.registerForm.username = ''
      this.registerForm.password = ''
      this.registerForm.repassword = ''
      this.registerForm.moblie = ''
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
.register-form {
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
