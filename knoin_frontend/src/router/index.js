import Vue from 'vue'
import VueRouter from 'vue-router'

import Login from '@/views/login'
import Register from '@/views/register'
import Layout from '@/views/layout'
import Home from '@/views/layout/home'
import Project01 from '@/views/layout/project-01'
import Desc01 from '@/views/layout/project-01/desc.vue'
import Result01 from '@/views/layout/project-01/result.vue'
import Project02 from '@/views/layout/project-02'
import Help from '@/views/layout/help'
import Upload from '@/views/layout/upload'

// import { verify } from '@/api/user.js'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/',
    component: Layout,
    children: [
      { // 主页
        path: '',
        name: 'Home',
        component: Home
      },
      { // 帮助
        path: '/help',
        name: 'Help',
        component: Help
      },
      { // 文件上传
        path: '/upload',
        name: 'Upload',
        component: Upload
      },
      { // 01项目页
        path: '/project-01',
        component: Project01,
        children: [
          {
            path: '',
            name: 'Desc01',
            component: Desc01
          },
          {
            path: 'result',
            name: 'Result01',
            component: Result01
          }
        ]
      },
      { // 02项目页
        path: '/project-02',
        name: 'Project02',
        component: Project02
      }
    ]
  }

]

const router = new VueRouter({
  routes
})

// router.beforeEach((to, from, next) => {
//   if (to.name !== 'Login' && to.name !== 'Register') {
//     const token = window.localStorage.getItem('token')
//     verify(token).then(res => {
//       next()
//     }).catch(err => {
//       if (err.response.status === 400) {
//         alert('登录过期，请重新登录')
//       }
//       next({ name: 'Login' })
//     })
//   } else { next() }
// })

export default router
