import axios from '@/libs/api.request'

const rackUrl = '/api/category/racks/'

export const GetRackList = (params) => {
  return axios.request({
    url: rackUrl,
    method: 'get',
    params: params
  })
}

export const GetRack = (id) => {
  return axios.request({
    url: rackUrl + id + '/',
    method: 'get'
  })
}

export const CreateRack = (data) => {
  return axios.request({
    url: rackUrl,
    method: 'post',
    data: data
  })
}

export const UpdateRack = (id, data) => {
  return axios.request({
    url: rackUrl + id + '/',
    method: 'put',
    data: data
  })
}

export const DeleteRack = (id) => {
  return axios.request({
    url: rackUrl + id + '/',
    method: 'delete'
  })
}
