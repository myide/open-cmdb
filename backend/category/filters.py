# -*- coding: utf-8 -*-
from utils.basefilters import BaseFilter

from .models import *


class IdcFilter(BaseFilter):

    class Meta:
        model = Idc
        fields = {
            'name': ['icontains'],
            'address': ['icontains']
        }


class ServerFilter(BaseFilter):

    class Meta:
        model = Server
        fields = {
            'name': ['icontains'],
            'ssh_ip': ['icontains']
        }
