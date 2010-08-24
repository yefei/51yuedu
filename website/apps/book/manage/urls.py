# -*- coding: utf-8 -*-
# Created on 2010-3-17
# @author: Yefe
# $Id$
from django.conf.urls.defaults import patterns, url
from website.apps.book.manage import views

urlpatterns = patterns('',
    url(r'^$',                      views.index,      name='index'),
    url(r'^add/$',                  views.add,      name='add'),
    url(r'^(?P<id>\d+)/$',          views.book,      name='book'),
    url(r'^chapter/(?P<id>\d+)/$',  views.chapter,      name='chapter'),
    url(r'^(?P<book_id>\d+)/add/$',          views.chapter_add,      name='chapter_add'),
    url(r'^(?P<id>\d+)/delete/$',      views.delete,      name='delete'),
)
