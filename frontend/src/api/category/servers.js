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

export const FetchServerInfo = (id) => {
  return axios.request({
    url: serverUrl + id + '/info/',
    method: 'get'
  })
}

export const FetchServerCron = (id, data) => {
  return axios.request({
    url: serverUrl + id + '/fetch_cron_content/',
    method: 'post',
    data: data
  })
}

export const FetchServerCronLog = (id, data) => {
  return axios.request({
    url: serverUrl + id + '/fetch_cron_log/',
    method: 'post',
    data: data
  })
}

export const UpdateServerCron = (id, data) => {
  return axios.request({
    url: serverUrl + id + '/update_cron_file/',
    method: 'post',
    data: data
  })
}

export const SyncServerCron = (id, data) => {
  return axios.request({
    url: serverUrl + id + '/sync_cron_file/',
    method: 'post',
    data: data
  })
}
