import Vue from 'vue'
import Cookies from 'js-cookie'
import Router from 'vue-router'
import routes from './routers'
import iView from 'iview'
import { setTitle } from '@/libs/util'

Vue.use(Router)
const router = new Router({
  routes,
  mode: 'history'
})

router.beforeEach((to, from, next) => {
  iView.LoadingBar.start()
  const token = Cookies.get('token')
  if (token) {
    next()
  } else {
    if (to.name === 'login') next()
    else next({ name: 'login' })
  }
})

router.afterEach(to => {
  setTitle(to, router.app)
  iView.LoadingBar.finish()
  window.scrollTo(0, 0)
})

export default router
