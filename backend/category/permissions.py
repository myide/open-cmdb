# -*- coding: utf-8 -*-
from rest_framework import permissions


class ServerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser:
            return True
        return user in obj.users.all()
