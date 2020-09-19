from django.contrib import admin

from .models import BusinessLine
from .models import Idc
from .models import Project
from .models import Rack
from .models import Server
from .models import SSHUser

# Register your models here.


@admin.register(SSHUser)
class SSHUserAdmin(admin.ModelAdmin):
    ordering = ('id',)


@admin.register(Idc)
class IdcAdmin(admin.ModelAdmin):
    ordering = ('id',)


@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    ordering = ('id',)


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    ordering = ('id',)


@admin.register(BusinessLine)
class BusinessLineAdmin(admin.ModelAdmin):
    ordering = ('id',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    ordering = ('id',)
