import axios from '@/libs/api.request'

export const Login = (data) => {
  return axios.request({
    url: '/api/api-token-auth/',
    method: 'post',
    data: data
  })
}

export const UnifiedAuth = (data) => {
  return axios.request({
    url: '/api/account/unitaryauth/',
    method: 'post',
    data: data
  })
}
