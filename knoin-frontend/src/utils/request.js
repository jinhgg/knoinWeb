import axios from 'axios'

const request = axios.create({
  baseURL: 'http://www.knoindx.com/'
})

export default request
