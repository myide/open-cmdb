import axios from '@/libs/api.request'

const businessLineUrl = '/api/category/businesslines/'

export const GetBusinessLineList = (params) => {
  return axios.request({
    url: businessLineUrl,
    method: 'get',
    params: params
  })
}

export const GetBusinessLine = (id) => {
  return axios.request({
    url: businessLineUrl + id + '/',
    method: 'get'
  })
}

export const CreateBusinessLine = (data) => {
  return axios.request({
    url: businessLineUrl,
    method: 'post',
    data: data
  })
}

export const UpdateBusinessLine = (id, data) => {
  return axios.request({
    url: businessLineUrl + id + '/',
    method: 'put',
    data: data
  })
}

export const DeleteBusinessLine = (id) => {
  return axios.request({
    url: businessLineUrl + id + '/',
    method: 'delete'
  })
}
