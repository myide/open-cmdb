import axios from '@/libs/api.request'

const historyUrl = '/api/history/histories/'

export const GetHistoryList = (params) => {
  return axios.request({
    url: historyUrl,
    method: 'get',
    params: params
  })
}

export const GetHistory = (id) => {
  return axios.request({
    url: historyUrl + id + '/',
    method: 'get'
  })
}
