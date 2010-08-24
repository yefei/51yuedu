# -*- coding: utf-8 -*-
# Created on 2010-3-6
# @author: Yefe
# $Id$
from django.contrib import admin
from website.apps.account.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'gender', 'online_seconds', 'is_admin', 'last_request_at', 'registered_at')
    list_filter = ('gender', 'is_admin')


admin.site.register(User, UserAdmin)
