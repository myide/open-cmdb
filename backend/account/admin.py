# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'remark',
    )

admin.site.register(User, UserAdmin)
