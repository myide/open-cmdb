# -*- coding: utf-8 -*-
import datetime

from croniter import croniter
from django.conf import settings
from django.forms.models import model_to_dict
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from history import LogType
from history.handlers import create_history
from utils.baseviews import BaseView

from .filters import *
from .permissions import *
from .serializers import *


class IdcViewSet(BaseView):
    """
    机房
    """
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer
    search_fields = ['name', 'address']
    filter_class = IdcFilter


class RackViewSet(BaseView):
    """
    机柜
    """
    queryset = Rack.objects.all()
    serializer_class = RackSerializer
    search_fields = ['name', 'ssh_ip']


class ServerViewSet(BaseView):
    """
    服务器
    """
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    filter_class = ServerFilter
    search_fields = ['name', 'ssh_ip']
    permission_classes = [ServerPermission]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ServerDetailSerializer
        return ServerListSerializer

    def perform_create(self, serializer):
        super(ServerViewSet, self).perform_create(serializer)
        log_data = dict(
            name=LogType.CRATE_SERVER,
            user=self.request.user,
            instance='',
            before='',
            after=serializer.data
        )
        create_history(**log_data)

    def perform_update(self, serializer):
        instance = self.get_object()
        super(ServerViewSet, self).perform_update(serializer)
        log_data = dict(
            name=LogType.UPDATE_SERVER,
            user=self.request.user,
            instance=instance.ssh_ip,
            before=self.serializer_class(instance).data,
            after=serializer.data
        )
        create_history(**log_data)

    def perform_destroy(self, instance):
        ssh_ip = instance.ssh_ip
        before = self.serializer_class(instance).data
        super(ServerViewSet, self).perform_destroy(instance)
        log_data = dict(
            name=LogType.DELETE_SERVER,
            user=self.request.user,
            instance=ssh_ip,
            before=before,
            after=''
        )
        create_history(**log_data)

    @action(methods=['get'], detail=True)
    def info(self, request, pk=None):
        instance = self.get_object()
        ssh_operation = SSHOperation(instance.ssh_ip, instance.ssh_port, instance.ssh_user.name)
        data_server = model_to_dict(instance)
        data_server = ssh_operation.fetch_host_info(data_server, instance.ssh_user.name)
        data_server.pop('users')
        Server.objects.filter(pk=pk).update(**data_server)
        return Response({})

    @action(methods=['post'], detail=True)
    def fetch_cron_content(self, request, pk=None):
        data = request.data
        instance = self.get_object()
        ssh_operation = SSHOperation(instance.ssh_ip, instance.ssh_port, instance.ssh_user.name)
        data = ssh_operation.fetch_cron_content(data['name'])
        return Response({'data': data})

    @action(methods=['post'], detail=True)
    def update_cron_file(self, request, pk=None):
        data = request.data
        after = data.get('content', '')
        cron_rules = after.split('\n')
        for cron in cron_rules:
            if cron.strip():
                rule = ' '.join(cron.split()[:5])
                try:
                    croniter(rule, datetime.datetime.now())
                except Exception as e:
                    raise ParseError(e)
        instance = self.get_object()
        ssh_operation = SSHOperation(instance.ssh_ip, instance.ssh_port, instance.ssh_user.name)
        before = ssh_operation.fetch_cron_content(instance.ssh_user)
        ssh_operation.update_cron_file(data['name'], data['content'])
        log_data = dict(
            name=LogType.UPDATE_CRON,
            user=self.request.user,
            instance=instance.ssh_ip,
            before=before,
            after=after
        )
        create_history(**log_data)
        return Response(self.serializer_class(instance).data)

    @action(methods=['post'], detail=True)
    def fetch_cron_log(self, request, pk=None):
        data = request.data
        instance = self.get_object()
        ssh_operation = SSHOperation(instance.ssh_ip, instance.ssh_port, instance.ssh_user.name)
        data = ssh_operation.fetch_cron_log(instance.ssh_user.name, data['count'])
        return Response({'data': data})

    @action(methods=['post'], detail=True)
    def sync_cron_file(self, request, pk=None):
        data = request.data
        instance = self.get_object()
        ssh_operation = SSHOperation(instance.ssh_ip, instance.ssh_port, instance.ssh_user.name)
        content = ssh_operation.fetch_cron_content(instance.ssh_user)
        ips = ssh_operation.sync_cron_file(instance.ssh_user.name, data)
        log_data = dict(
            name=LogType.SYNC_CRON,
            user=self.request.user,
            instance=instance.ssh_ip,
            before=content,
            after=content,
            remark='目标服务器:\n{}'.format(str(ips))
        )
        create_history(**log_data)
        return Response(self.serializer_class(instance).data)


class SSHUserViewSet(BaseView):
    """
    SSH用户
    """
    queryset = SSHUser.objects.all()
    serializer_class = SSHUserSerializer
    search_fields = ['name']


class BusinessLineViewSet(BaseView):
    """
    业务线
    """
    queryset = BusinessLine.objects.all()
    serializer_class = BusinessLineSerializer
    search_fields = ['name']


class ProjectViewSet(BaseView):
    """
    项目
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    search_fields = ['name']


class APIDashBoardView(APIView):
    """
    报表页
    """
    model_idc = Idc
    model_server = Server
    model_business = BusinessLine
    model_project = Project
    model_user = User

    def get_queryset(self, model):
        return model.objects.all()

    def get(self, request, *args, **kwargs):
        data = dict()
        qs_idc = self.get_queryset(self.model_idc)
        qs_server = self.get_queryset(self.model_server)
        qs_business = self.get_queryset(self.model_business)
        qs_project = self.get_queryset(self.model_project)
        qs_user = self.get_queryset(self.model_user)

        pie = list()
        for idc in qs_idc:
            idc_server_count = 0
            for rack in idc.rack_set.all():
                idc_server_count += rack.server_set.count()
            pie.append({'name': idc.name, 'value': idc_server_count})
        data['pie'] = pie

        info = dict()
        info['server_count'] = qs_server.count()
        info['business_count'] = qs_business.count()
        info['project_count'] = qs_project.count()
        info['user_count'] = qs_user.count()
        data['info'] = info

        date_login = dict()
        date_list = list()
        for i in range(7, 0, -1):
            date_time = datetime.datetime.now() - datetime.timedelta(days=i)
            date_list.append(date_time.strftime("%Y-%m-%d"))
        qs_user_date = qs_user.filter(last_login__gte=date_list[0])
        for date in date_list:
            num = 0
            for user in qs_user_date:
                if date in user.last_login.strftime("%Y-%m-%d"):
                    num += 1
            date_login[date] = num
        data['date_login'] = date_login

        return Response({'data': data})


class APILocalSSHUserView(APIView):
    """
    settings设置的本地SSH用户
    """
    def get(self, request):
        local_ssh_user = settings.LOCAL_SSH_USER
        return Response({'data': local_ssh_user})
