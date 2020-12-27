import axios from 'axios'

const request = axios.create({
  baseURL: 'http://127.0.0.1:8000/'
})

// axios拦截器
request.interceptors.request.use(
  function (config) {
    // 注册页面不加Authorization
    if (config.url === '/users/' && config.method === 'post') {
      return config
    }

    const token = window.localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `jwt ${token}`
    }
    return config
  },
  function (error) {
    return Promise.reject(error)
  }
)

// 响应拦截器
// Add a response interceptor
request.interceptors.response.use(function (res) {
  // 所有响应码为 2xx 的响应都会进入这里
  // response 是响应处理
  // 注意：一定要把响应结果 return，否则真正发请求的位置拿不到数据
  if ('token' in res.data) {
    window.localStorage.setItem('token', res.data.token)
  }
  return res
}, function (error) {
  const { status } = error.response
  // 任何超出 2xx 的响应码都会进入这里
  if (status === 401) {
    // 跳转到登录页面
    // 清除本地存储中的用户登录状态
    // window.localStorage.removeItem('user')
    // router.push('/login')
  } else if (status === 403) {
    // token 未携带或已过期

  } else if (status === 400) {
    // 客户端参数错误
  } else if (status >= 500) {
  }

  return Promise.reject(error)
})

export default request
