# -*- coding: utf-8 -*-
from django.db import models


class BaseModel(models.Model):
    '''
       基础表(抽象类)
    '''
    name = models.CharField(default='', null=True, blank=True, max_length=128, verbose_name='名字')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    remark = models.TextField(default='', null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        abstract = True
