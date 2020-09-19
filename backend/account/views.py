# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.baseviews import BaseView
from utils.permissions import IsSuperUser
from utils.unitaryauth import UnitaryAuth
from utils.wrappers import permission_admin

from .serializers import *


class GroupViewSet(BaseView):
    """
    系统组CURD
    """
    queryset = Group.objects.order_by('-id')
    serializer_class = GroupSerializer
    permission_classes = [IsSuperUser]
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.create(self.request.data)

    def perform_update(self, serializer):
        serializer.update(self.get_object(), self.request.data)


class UserViewSet(BaseView):
    """
    系统用户CURD
    """
    queryset = User.objects.filter(is_staff=True).order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]
    search_fields = ['username']

    def perform_update(self, serializer):
        # 有额外字段，所以绕开了默认的序列化、save那一套；不然的话额外字段会被删除。下同:
        serializer.update(self.get_object(), self.request.data)

    @permission_admin
    def perform_create(self, serializer):
        serializer.create(self.request.data)

    @permission_admin
    def perform_destroy(self, instance):
        instance.delete()


class UnitaryAuthView(UnitaryAuth, APIView):
    """
    接入统一登录
    """
    serializer_class = UserSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        if not self.authenticate:
            raise AuthenticationFailed
        request.data.update({'is_staff': True})
        serializer = self.serializer_class(data=request.data)
        user_query = self.serializer_class.Meta.model.objects.filter(username=request.data.get('username'))
        if user_query:
            serializer = self.serializer_class(user_query[0], data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
