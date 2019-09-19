import axios from '@/libs/api.request'

const projectUrl = '/api/category/projects/'

export const GetProjectList = (params) => {
  return axios.request({
    url: projectUrl,
    method: 'get',
    params: params
  })
}

export const GetProject = (id) => {
  return axios.request({
    url: projectUrl + id + '/',
    method: 'get'
  })
}

export const CreateProject = (data) => {
  return axios.request({
    url: projectUrl,
    method: 'post',
    data: data
  })
}

export const UpdateProject = (id, data) => {
  return axios.request({
    url: projectUrl + id + '/',
    method: 'put',
    data: data
  })
}

export const DeleteProject = (id) => {
  return axios.request({
    url: projectUrl + id + '/',
    method: 'delete'
  })
}
