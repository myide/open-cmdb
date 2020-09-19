# -*- coding: utf-8 -*-
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated


class ReturnFormatMixin(object):

    @classmethod
    def get_ret(cls):
        return {'status': 0, 'msg': '', 'data': {}}


class BasePagination(PageNumberPagination):
    page_size_query_param = 'pagesize'
    page_query_param = 'page'
    max_page_size = 1000


class DefaultPagination(BasePagination):
    page_size = 10


class MaxSizePagination(BasePagination):
    page_size = 1000


class BaseView(viewsets.ModelViewSet):
    queryset = None
    serializer_class = None
    permission_classes = [IsAuthenticated]
    # 分页
    pagination_class = DefaultPagination
    # 搜索
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = []  # 用于单一搜索：接收前端的search参数，从多个字段中匹配，或的关系
    filter_class = None  # 用于综合搜索：可接收前端的多个查询参数，对相应的字段匹配，且的关系
