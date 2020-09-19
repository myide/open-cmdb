# -*- coding:utf-8 -*-
from rest_framework import serializers

from .models import *


class HistorySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = History
        fields = '__all__'

    def get_user(self, instance):
        return instance.user.username
