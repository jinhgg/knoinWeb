import request from '@/utils/request'

// 登录
export const login = data => {
  return request({
    method: 'POST',
    url: '/token-auth/',
    data
  })
}
// 校验权限
export const verify = token => {
  return request({
    method: 'POST',
    url: '/token-refresh/',
    data: { token }
  })
}
// 注册
export const register = data => {
  return request({
    method: 'POST',
    url: '/users/',
    data
  })
}
// 获取用户详情
export const getUser = userId => {
  return request({
    method: 'GET',
    url: `/users/${userId}`
  })
}

// 表单校验
// export const checkRegister = data => {
//   return request({
//     method: 'POST',
//     url: '/checkRegister',
//     data
//   })
// }
