# -*- coding:utf-8 -*-
from django.contrib.auth.models import Group
from collections import OrderedDict
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['user_permissions']

    def to_representation(self, instance):
        ret = super(UserSerializer, self).to_representation(instance)
        if not isinstance(instance, OrderedDict):
            group_instance = instance.groups.first()
            groups = {'id': group_instance.id, 'name': group_instance.name} if group_instance else {}
            ret['groups'] = groups
        return ret

    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if instance.password != password:
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        exclude = ['permissions']

    def to_representation(self, instance):
        ret = super(GroupSerializer, self).to_representation(instance)
        if not isinstance(instance, OrderedDict):
            member_set = instance.user_set.all()
            members = [{'id': user.id, 'name': user.username, 'role': user.role} for user in member_set]
            ret['members'] = members
        return ret
