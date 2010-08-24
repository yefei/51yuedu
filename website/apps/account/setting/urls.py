# Create by: Yefe @ 2009-8-17
# Django urls
# $Id$

from django.conf.urls.defaults import patterns, url
from website.apps.account.setting import views

urlpatterns = patterns('',
    url(r'^$',                  views.index,      name='index'),
    url(r'^function/$',         views.function,    name='function'),
    url(r'^profile/$',          views.profile,    name='profile'),
    url(r'^avatar/$',           views.avatar,     name='avatar'),
    url(r'^password/$',         views.password,   name='password'),
    url(r'^email/$',            views.email,      name='email'),
)
