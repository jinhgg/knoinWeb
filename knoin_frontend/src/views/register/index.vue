<template>
  <div>
    <b-card class="register-form" header="南京诺因生物—临床检测分析报告系统">
      <b-form @submit="onSubmit" @reset="onReset" v-if="show">
        <b-form-group id="input-group-1" label="用户名:" label-for="input-1">
          <b-form-input
            id="input-1"
            v-model="registerForm.username"
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
            v-model="registerForm.password"
            type="password"
            :state="validForm.password.isValid"
            required
          ></b-form-input>
          <b-form-invalid-feedback>
            {{ validForm.password.info }}
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group id="input-group-3" label="重复密码:" label-for="input-3">
          <b-form-input
            id="input-3"
            v-model="registerForm.password2"
            type="password"
            :state="validForm.password2.isValid"
            required
          ></b-form-input>
          <b-form-invalid-feedback>
            {{ validForm.password2.info }}
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group id="input-group-4" label="手机号:" label-for="input-4">
          <b-form-input
            id="input-4"
            v-model="registerForm.mobile"
            type="tel"
            :state="validForm.mobile.isValid"
            required
          ></b-form-input>
          <b-form-invalid-feedback>
            {{ validForm.mobile.info }}
          </b-form-invalid-feedback>
        </b-form-group>
        <div class="button-group">
          <b-button type="submit" variant="primary">注册</b-button>
          <b-button type="reset" variant="danger">重置</b-button>
        </div>
      </b-form>
      <!-- <b-card class="mt-3" header="Form Data Result">
        <pre class="m-0">{{ registerForm }}</pre>
      </b-card> -->
    </b-card>
  </div>
</template>

<script>
import { register } from '@/api/user'

export default {
  name: 'Register',
  data() {
    return {
      registerForm: {
        username: '',
        password: '',
        password2: '',
        mobile: ''
      },
      validForm: {
        username: { isValid: null, info: '' },
        password: { isValid: null, info: '' },
        password2: { isValid: null, info: '' },
        mobile: { isValid: null, info: '' }
      },
      show: true
    }
  },
  methods: {
    checkForm() {
      const registerForm = this.registerForm
      const vaildForm = this.validForm
      let vaild = true
      if (registerForm.username.length < 3 || registerForm.username.length > 50) {
        vaildForm.username = { isValid: false, info: '用户名应在3~50位之间' }
        vaild = false
      }
      if (registerForm.password.length < 3) {
        vaildForm.password = { isValid: false, info: '密码长度不能小于3位' }
        vaild = false
      }
      if (registerForm.password !== registerForm.password2) {
        vaildForm.password2 = { isValid: false, info: '两次密码输入不一致' }
        vaild = false
      }
      if (registerForm.mobile.length !== 11) {
        vaildForm.mobile = { isValid: false, info: '手机号格式不正确' }
        vaild = false
      }
      return vaild
    },
    showErrMsg(msg) {
      this.resetValidForm()
      const validForm = this.validForm
      Object.keys(msg).forEach(function (key) {
        validForm[key] = {
          isValid: false, info: msg[key][0]
        }
      })
    },
    resetValidForm() {
      this.validForm = {
        username: { isValid: null, info: '' },
        password: { isValid: null, info: '' },
        password2: { isValid: null, info: '' },
        mobile: { isValid: null, info: '' }
      }
    },
    onSubmit(evt) {
      evt.preventDefault()
      this.resetValidForm()
      if (this.checkForm() === false) { return }
      register(this.registerForm).then(res => {
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
      this.resetValidForm()
      this.registerForm.username = ''
      this.registerForm.password = ''
      this.registerForm.password2 = ''
      this.registerForm.mobile = ''
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
