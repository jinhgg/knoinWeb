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
          <b-form-invalid-feedback>
            {{ validation.username.info }}
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
          <b-form-invalid-feedback>
            {{ validation.password.info }}
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group id="input-group-3" label="重复密码:" label-for="input-3">
          <b-form-input
            id="input-3"
            v-model="registerForm.password2"
            type="password"
            :state="validation.password2.isValid"
            required
          ></b-form-input>
          <b-form-invalid-feedback>
            {{ validation.password2.info }}
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group id="input-group-4" label="手机号:" label-for="input-4">
          <b-form-input
            id="input-4"
            v-model="registerForm.mobile"
            type="tel"
            :state="validation.mobile.isValid"
            required
          ></b-form-input>
          <b-form-invalid-feedback>
            {{ validation.mobile.info }}
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
      validation: {
        username: { isValid: null, info: '' },
        password: { isValid: null, info: '' },
        password2: { isValid: null, info: '' },
        mobile: { isValid: null, info: '' }
      },
      show: true
    }
  },
  methods: {
    resetValidation() {
      this.validation = {
        username: { isValid: null, info: '' },
        password: { isValid: null, info: '' },
        password2: { isValid: null, info: '' },
        mobile: { isValid: null, info: '' }
      }
    },

    onSubmit(evt) {
      evt.preventDefault()
      this.resetValidation()
      // alert(JSON.stringify(this.loginForm))
      register(this.registerForm).then(res => {
        console.log('注冊成功！')
      }).catch(err => {
        const errMsg = err.response.data
        console.log(errMsg)
        if (errMsg.mobile) {
          this.validation.mobile = {
            isValid: false, info: errMsg.mobile[0]
          }
        } else if (errMsg.non_field_errors) {
          this.validation.password2 = {
            isValid: false, info: errMsg.non_field_errors
          }
        } else if (errMsg.includes('Duplicate entry') && errMsg.includes('users_user.username')) {
          this.validation.username = {
            isValid: false, info: '用户名已注册'
          }
        } else if (errMsg.includes('Duplicate entry') && errMsg.includes('users_user_mobile')) {
          this.validation.mobile = {
            isValid: false, info: '手机号已注册'
          }
        } else {
          alert(errMsg)
        }
      })
    },
    onReset(evt) {
      evt.preventDefault()
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
