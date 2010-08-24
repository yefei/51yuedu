# Create by: Yefe @ 2009-8-17
# Django urls
# $Id$

from django.conf.urls.defaults import patterns, url, include
from website.apps.account import views

urlpatterns = patterns('',
    url(r'^$',                  views.index,      name='index'),
    url(r'^login/$',            views.login,      name='login'),
    url(r'^logout/$',           views.logout,     name='logout'),
    url(r'^register/$',         views.register,   name='register'),
    
    (r'^setting/', include('website.apps.account.setting.urls', 'setting')),
    (r'^forgot/', include('website.apps.account.forgot.urls', 'forgot')),
)

