import axios from '@/libs/api.request'

const sshUserUrl = '/api/category/sshusers/'
const LocalSSHUserUrl = '/api/category/api_local_ssh_user/'

export const GetSSHUserList = (params) => {
  return axios.request({
    url: sshUserUrl,
    method: 'get',
    params: params
  })
}

export const GetSSHUser = (id) => {
  return axios.request({
    url: sshUserUrl + id + '/',
    method: 'get'
  })
}

export const CreateSSHUser = (data) => {
  return axios.request({
    url: sshUserUrl,
    method: 'post',
    data: data
  })
}

export const UpdateSSHUser = (id, data) => {
  return axios.request({
    url: sshUserUrl + id + '/',
    method: 'put',
    data: data
  })
}

export const DeleteSSHUser = (id) => {
  return axios.request({
    url: sshUserUrl + id + '/',
    method: 'delete'
  })
}

export const GetLocalSSHUser = (data) => {
  return axios.request({
    url: LocalSSHUserUrl,
    method: 'get'
  })
}
