# Create your models here.
from django.db import models

from account.models import User
from utils.basemodels import BaseModel


class SSHUser(BaseModel):
    STATUS = (
        ('0', u'启用'),
        ('1', u'停用'),
    )
    password = models.CharField(default='', max_length=128, null=True, blank=True, verbose_name='SSH 密码')

    class Meta:
        ordering = ['-id']
        unique_together = ['name']


class Idc(BaseModel):
    address = models.CharField(max_length=256, verbose_name='地址')

    class Meta:
        ordering = ['-id']
        unique_together = ('name',)


class Rack(BaseModel):
    idc = models.ForeignKey(Idc, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属机房')
    number = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='编号')
    size = models.CharField(default='', max_length=8, null=True, blank=True, verbose_name='U型')

    class Meta:
        ordering = ['-id']
        unique_together = ('name', 'idc')


class Server(BaseModel):
    STATUS = (
        ('0', u'下线'),
        ('1', u'在线'),
    )
    users = models.ManyToManyField(User, default='', null=True, blank=True, verbose_name='业务相关的用户')
    rack = models.ForeignKey(Rack, default='', null=True, blank=True, on_delete=models.SET_DEFAULT, verbose_name='所属机柜')
    ssh_user = models.ForeignKey(SSHUser, default='', null=True, blank=True, on_delete=models.SET_DEFAULT, verbose_name='SSH用户')
    ssh_ip = models.CharField(default='', max_length=128, null=True, blank=True, verbose_name='SSH IP地址/主机名')
    ssh_port = models.IntegerField(default=22, max_length=5, null=True, blank=True, verbose_name='SSH 端口')
    uuid = models.CharField(default='', max_length=128, null=True, blank=True, verbose_name='UUID')
    cpu = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='CPU')
    memory = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='内存')
    disk = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='磁盘大小')
    system_product = models.CharField(default='', max_length=128, null=True, blank=True, verbose_name='服务器类型')
    daq = models.TextField(default='', null=True, blank=True, verbose_name='数据采集')
    status = models.CharField(default='1', max_length=2, choices=STATUS, verbose_name='运行状态')

    class Meta:
        ordering = ['-id']


class BusinessLine(BaseModel):
    users = models.ManyToManyField(User, default='', null=True, blank=True, verbose_name='相关用户')

    class Meta:
        ordering = ['-id']
        unique_together = ['name']


class Project(BaseModel):
    STATUS = (
        ('0', u'启用'),
        ('1', u'停用'),
    )
    LANGUAGE = (
        ('python', 'python'),
        ('java', 'java'),
        ('php', 'php'),
        ('golang', 'golang')
    )
    businesses = models.ManyToManyField(BusinessLine, default='', null=True, blank=True, verbose_name='所属业务线')
    users = models.ManyToManyField(User, default='', null=True, blank=True, verbose_name='相关用户')
    servers = models.ManyToManyField(Server, default='', null=True, blank=True, verbose_name='相关服务器')
    language_type = models.CharField(default='', max_length=256, choices=LANGUAGE, null=True, blank=True, verbose_name='语言类型')
    repo_url = models.CharField(default='', max_length=256, null=True, blank=True, verbose_name='版本库地址')
    jenkins_job = models.CharField(default='', max_length=128, null=True, blank=True, verbose_name='JENKINS JOB')
    status = models.CharField(default='0', max_length=2, choices=STATUS, verbose_name='状态')

    class Meta:
        ordering = ['-id']
        unique_together = ['name']
