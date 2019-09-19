# -*- coding: utf-8 -*-
import django_filters


class BaseFilter(django_filters.FilterSet):
    sort = django_filters.OrderingFilter(fields=('create_time',))

    class Meta:
        model = None
        fields = {}
