# -*- coding: utf-8 -*-
import json
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.baseviews import BaseView
from utils.permissions import IsSuperUser
from account.models import User
from .serializers import *
from .filters import *
from .permissions import *


class IdcViewSet(BaseView):
    """
    机房
    """
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer
    search_fields = ['name']
    filter_class = IdcFilter


class RackViewSet(BaseView):
    """
    机柜
    """
    queryset = Rack.objects.all()
    serializer_class = RackSerializer
    search_fields = ['name']


class ServerViewSet(BaseView):
    """
    服务器
    """
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    search_fields = ['name']
    permission_classes = [ServerPermission]


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


class ServerCollectView(APIView):
    """
    服务器信息采集
    """
    model = Server
    keys = ['name', 'cpu', 'memory', 'disk', 'uuid', 'server_type']
    permission_classes = []

    def post(self, request):
        data = request.data
        server_data = {key: data[key] for key in self.keys}
        server_data['daq'] = json.dumps(data)
        qs_instance = self.model.objects.filter(uuid=data.get('uuid'), server_type=data.get('server_type'))
        if qs_instance:
            qs_instance.update(**server_data)
            qs_instance.first().save()
        else:
            self.model.objects.create(**server_data)
        return Response({})


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
