import axios from 'axios'
import Cookies from 'js-cookie'
import iView from 'iview'
import router from '@/router'

function permerror (nodesc, title, desc) {
  iView.Notice.error({
    duration: 10,
    title: title,
    desc: nodesc ? '' : desc
  })
}

class HttpRequest {
  constructor (baseUrl = baseURL) {
    this.baseUrl = baseUrl
    this.queue = {}
  }

  getInsideConfig () {
    const config = {
      baseURL: this.baseUrl,
      headers: {}
    }
    return config
  }

  destroy (url) {
    delete this.queue[url]
    if (!Object.keys(this.queue).length) {
      // Spin.hide()
    }
  }

  interceptors (instance, url) {
    // 请求拦截
    instance.interceptors.request.use(config => {
      // 添加全局的loading...
      if (!Object.keys(this.queue).length) {
        // Spin.show() // 不建议开启，因为界面不友好
      }
      let token = Cookies.get('token')
      if (token) { // 获取到了本地的token
        config.headers.Authorization = 'JWT ' + token
      }
      this.queue[url] = true
      return config
    }, error => {
      return Promise.reject(error)
    })
    // 响应拦截
    instance.interceptors.response.use(res => {
      this.destroy(url)
      const { data, status } = res
      return { data, status }
    }, error => {
      if (error.response) {
        switch (error.response.status) {
          case 400:
            permerror(false, error.response.request.statusText, error.response.request.responseText)
            break
          case 401: // 拦截验证token失败的请求，清除token信息并跳转到登录页面
            router.push({
              name: 'login'
            })
            break
          case 403:
            permerror(false, error.response.statusText, error.response.data.detail)
            break
          case 500:
            permerror(false, error.response.status, error.response.statusText)
            break
        }
      }
      return Promise.reject(error)
    })
  }

  request (options) {
    const instance = axios.create()
    options = Object.assign(this.getInsideConfig(), options)
    this.interceptors(instance, options.url)
    return instance(options)
  }
}
export default HttpRequest
