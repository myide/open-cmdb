import axios from '@/libs/api.request'

const idcUrl = '/api/category/idcs/'

export const GetIdcList = (params) => {
  return axios.request({
    url: idcUrl,
    method: 'get',
    params: params
  })
}

export const GetIdc = (id) => {
  return axios.request({
    url: idcUrl + id + '/',
    method: 'get'
  })
}

export const CreateIdc = (data) => {
  return axios.request({
    url: idcUrl,
    method: 'post',
    data: data
  })
}

export const UpdateIdc = (id, data) => {
  return axios.request({
    url: idcUrl + id + '/',
    method: 'put',
    data: data
  })
}

export const DeleteIdc = (id) => {
  return axios.request({
    url: idcUrl + id + '/',
    method: 'delete'
  })
}
