# -*- coding: utf-8 -*-
from utils.basefilters import BaseFilter
from .models import *


class IdcFilter(BaseFilter):

    class Meta:
        model = Idc
        fields = {
            'name': ['icontains'],
            'address': ['exact']
        }
