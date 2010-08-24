# -*- coding: utf-8 -*-
# Created on 2010-3-17
# @author: Yefe
# $Id$
from django.conf.urls.defaults import patterns, url
from website.apps.about import views

urlpatterns = patterns('',
    #url(r'^$',                      views.index,      name='index'),
    url(r'^feedback/$',    views.feedback,        name='feedback'),
)
