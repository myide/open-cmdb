from django.db import models

from account.models import User
from utils.basemodels import BaseModel

# Create your models here.


class History(BaseModel):
    user = models.ForeignKey(User, default='', null=True, blank=True, on_delete=models.SET_DEFAULT, verbose_name='用户')
    instance = models.CharField(default='', max_length=32, null=True, blank=True, verbose_name='对象')
    before = models.TextField(default='', null=True, blank=True, verbose_name='操作前')
    after = models.TextField(default='', null=True, blank=True, verbose_name='操作后')

    class Meta:
        ordering = ['-id']
