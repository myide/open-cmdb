# -*- coding:utf-8 -*-
from collections import OrderedDict
from rest_framework import serializers
from .models import *


class IdcSerializer(serializers.ModelSerializer):

    class Meta:
        model = Idc
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        racks = instance.rack_set.values('id', 'name')
        ret['racks'] = racks
        return ret


class RackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rack
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        servers = instance.server_set.values('id', 'name')
        ret['servers'] = servers
        idc = instance.idc
        ret['idc_name'] = idc.name if idc else None
        return ret


class ServerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Server
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        rack = instance.rack
        if rack:
            rack_name = rack.name
            idc = rack.idc_id
            idc_name = rack.idc.name if rack.idc else None
        else:
            rack_name = idc = idc_name = None
        ret['rack_name'] = rack_name
        ret['idc'] = idc
        ret['idc_name'] = idc_name
        ret['users'] = instance.users.values('id', 'username')
        ret['ssh_users'] = instance.ssh_users.values('id', 'name')
        ret['projects'] = instance.project_set.values('id', 'name')
        return ret


class SSHUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = SSHUser
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['servers'] = instance.server_set.values('id', 'name')
        return ret


class BusinessLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessLine
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['users'] = instance.users.values('id', 'username')
        ret['projects'] = instance.project_set.values('id', 'name')
        return ret


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['businesses'] = instance.businesses.values('id', 'name')
        ret['users'] = instance.users.values('id', 'username')
        ret['servers'] = instance.servers.values('id', 'name')
        return ret
