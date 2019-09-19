import axios from '@/libs/api.request'

const dashBoardUrl = '/api/category/api_dashboard/'

export const GetDashBoardData = (params) => {
  return axios.request({
    url: dashBoardUrl,
    method: 'get',
    params: params
  })
}
