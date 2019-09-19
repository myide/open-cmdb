import axios from '@/libs/api.request'

const userUrl = '/api/account/users/'

export const GetUserList = (params) => {
  return axios.request({
    url: userUrl,
    method: 'get',
    params: params
  })
}

export const GetUser = (id) => {
  return axios.request({
    url: userUrl + id + '/',
    method: 'get'
  })
}

export const CreateUser = (data) => {
  return axios.request({
    url: userUrl,
    method: 'post',
    data: data
  })
}

export const UpdateUser = (id, data) => {
  return axios.request({
    url: userUrl + id + '/',
    method: 'put',
    data: data
  })
}

export const DeleteUser = (id) => {
  return axios.request({
    url: userUrl + id + '/',
    method: 'delete'
  })
}
