# -*- coding: utf-8 -*-
# Created on 2010-5-29
# @author: Yefe
# $Id$
from django.conf.urls.defaults import patterns, url, include
from website.apps.book import views

urlpatterns = patterns('',
    url(r'^$',                  views.index,      name='index'),
    url(r'^page-(?P<page>\d+)/$',                  views.index,      name='index_page'),
    url(r'^s(?P<subarea_id>\d+)/$',     views.books,      name='books_subarea'),
    url(r'^c(?P<category_id>\d+)/$',     views.books,      name='books_category'),
    url(r'^s(?P<subarea_id>\d+)-(?P<page>\d+)/$',     views.books,      name='books_subarea_page'),
    url(r'^c(?P<category_id>\d+)-(?P<page>\d+)/$',     views.books,      name='books_category_page'),
    url(r'^(?P<id>\d+)/$',     views.show,      name='show'),
    url(r'^(?P<id>\d+)/review/$',     views.review,      name='review'),
    url(r'^(?P<id>\d+)/review/new/$',     views.review_new,      name='review_new'),
    url(r'^(?P<id>\d+)/download/$',     views.download,      name='download'),
    url(r'^(?P<id>\d+)/download/(?P<encode>gbk|utf\-8)/.*?\.(?P<format>txt)$',
            views.download_start,      name='download_start'),
    url(r'^chapter/(?P<id>\d+)/$',     views.chapter,      name='chapter'),
    url(r'^read_point/$',     views.read_point,      name='read_point'),
    url(r'^favorite/$',     views.favorite,      name='favorite'),
    
    (r'^manage/',     include('website.apps.book.manage.urls',     'manage')),
)

