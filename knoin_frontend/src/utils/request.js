import axios from 'axios'

const request = axios.create({
  baseURL: 'http://127.0.0.1:8000/'
})

// axios拦截器
request.interceptors.request.use(
  function(config) {
    console.log(config)
    return config
  },
  function(error) {
    return Promise.reject(error)
  }
)

export default request
