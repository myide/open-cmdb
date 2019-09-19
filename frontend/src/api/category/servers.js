import axios from '@/libs/api.request'

const serverUrl = '/api/category/servers/'

export const GetServerList = (params) => {
  return axios.request({
    url: serverUrl,
    method: 'get',
    params: params
  })
}

export const GetServer = (id) => {
  return axios.request({
    url: serverUrl + id + '/',
    method: 'get'
  })
}

export const CreateServer = (data) => {
  return axios.request({
    url: serverUrl,
    method: 'post',
    data: data
  })
}

export const UpdateServer = (id, data) => {
  return axios.request({
    url: serverUrl + id + '/',
    method: 'put',
    data: data
  })
}

export const DeleteServer = (id) => {
  return axios.request({
    url: serverUrl + id + '/',
    method: 'delete'
  })
}
