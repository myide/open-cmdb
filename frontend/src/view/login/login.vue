<style lang="less">
  @import './login.less';
</style>

<template>
  <div class="login">
    <div class="login-con">
      <Card icon="log-in" title="欢迎登录" :bordered="false">
        <div class="form-con">
          <login-form @on-success-valid="handleSubmit"></login-form>
          <p class="login-tip">输入任意用户名和密码即可</p>
        </div>
      </Card>
    </div>
  </div>
</template>

<script>
import LoginForm from '_c/login-form'
import { mapActions } from 'vuex'
import {Login, UnifiedAuth} from '@/api/login'
import Cookies from 'js-cookie'

export default {
  components: {
    LoginForm
  },
  methods: {
    ...mapActions([
      'handleLogin',
      'getUserInfo'
    ]),


    UnifiedLogin (username, password) {
      const data = { username: username, password: password }
      UnifiedAuth(data)
      .then(response => {
        this.CommonLogin(username, password)
      })
    },
    CommonLogin (username, password) {
      const data = { username: username, password: password }
      Login(data)
      .then(response => {
        let token = response.data.token
        // cookie写入信息
        Cookies.set('token',token)
        Cookies.set('user', username);
        Cookies.set('password', password);
        localStorage.setItem('user', username)
        // 跳转到首页
        this.$router.push({
            name: '_home'
        });
        // 显示提示信息
        this.$Message.success({
            content: '登陆成功',
            duration: 3
        });
      })
    },
    handleSubmit ({ userName, password, loginType}) {
        if (loginType == 'unified') {
          console.log(111)
          this.UnifiedLogin(userName, password)
        } else {
          console.log(222)
          this.CommonLogin(userName, password)
        }
    }
  }
}
</script>

<style>
</style>
