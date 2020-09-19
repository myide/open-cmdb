# -*- coding: utf-8 -*-

from utils.baseviews import BaseView

from .models import *
from .serializers import *


class HistoryViewSet(BaseView):
    """
    历史记录
    """
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    search_fields = ['name']
