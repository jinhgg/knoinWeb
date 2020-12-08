import axios from 'axios'

const request = axios.create({
  baseURL: 'https://www.knoindx.com/'
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
