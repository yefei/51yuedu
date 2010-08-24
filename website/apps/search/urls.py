# -*- coding: utf-8 -*-
# Created on 2010-3-17
# @author: Yefe
# $Id$
from django.conf.urls.defaults import patterns, url
from website.apps.search import views

urlpatterns = patterns('',
    #url(r'^$',                      views.index,      name='index'),
    url(r'^(?P<applabel>\w+)/$',    views.app,        name='app'),
    url(r'^(?P<applabel>\w+)/(?P<word>.*?)/$',    views.app,        name='app_word'),
)
