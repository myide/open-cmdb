# -*- coding: utf-8 -*-
from utils.ldaptools import LdapAuth


class UnitaryAuth(object):

    @property
    def authenticate(self):
        '''
            1. 请求认证接口, 入参：需要根据接口的定义, 一般是 用户名(username), 密码(password)
            2. 接口认证成功，本方法返回True， 失败返回False
            :return: True/False
        '''
        data = self.request.data
        ldap = LdapAuth()
        ret = ldap.check(data.get('username'), data.get('password'))
        status = ret['status']
        return True if status == 0 else False
