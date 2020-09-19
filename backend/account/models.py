# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('developer_supremo', u'总监'),
        ('developer_manager', u'经理'),
        ('developer', u'研发'),
    )
    role = models.CharField(max_length=32, default='developer', choices=ROLES)
    remark = models.CharField(max_length=128, default='', blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = u'用户'

    def __unicode__(self):
        return self.username
