import Vue from 'vue'
import VueRouter from 'vue-router'

import Login from '@/views/login'
import Register from '@/views/register'
import Home from '@/views/home'
import Layout from '@/views/layout'

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
      {
        path: '',
        name: 'Home',
        component: Home
      }
    ]
  }
]

const router = new VueRouter({
  routes
})

export default router
