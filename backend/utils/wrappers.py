# -*- coding: utf-8 -*-
import logging
import time
from functools import wraps

from django.db import close_old_connections
from rest_framework.exceptions import ParseError
from rest_framework.exceptions import PermissionDenied


def permission_admin(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return func(self, *args, **kwargs)
        raise PermissionDenied
    return wrapper
