# -*- coding: utf-8 -*-
# Created on 2010-6-13
# @author: Yefe
# $Id$
from django.contrib import admin
from website.apps.about.models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact', 'created_at', 'ip')

admin.site.register(Feedback, FeedbackAdmin)
