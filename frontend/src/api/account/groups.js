import axios from '@/libs/api.request'

const groupUrl = '/api/account/groups/'

export const GetGroupList = (params) => {
  return axios.request({
    url: groupUrl,
    method: 'get',
    params: params
  })
}

export const GetGroup = (id) => {
  return axios.request({
    url: groupUrl + id + '/',
    method: 'get'
  })
}

export const CreateGroup = (data) => {
  return axios.request({
    url: groupUrl,
    method: 'post',
    data: data
  })
}

export const UpdateGroup = (id, data) => {
  return axios.request({
    url: groupUrl + id + '/',
    method: 'put',
    data: data
  })
}

export const DeleteGroup = (id) => {
  return axios.request({
    url: groupUrl + id + '/',
    method: 'delete'
  })
}
