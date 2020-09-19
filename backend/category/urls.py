# -*- coding: utf-8 -*-
from django.conf.urls import include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import *

# register的可选参数 base_name: 用来生成urls名字，如果viewset中没有包含queryset, base_name一定要有

router = DefaultRouter()
router.register(r'idcs', IdcViewSet)
router.register(r'racks', RackViewSet)
router.register(r'servers', ServerViewSet)
router.register(r'sshusers', SSHUserViewSet)
router.register(r'businesslines', BusinessLineViewSet)
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api_dashboard/$', APIDashBoardView.as_view()),
    url(r'^api_local_ssh_user/$', APILocalSSHUserView.as_view()),
]
