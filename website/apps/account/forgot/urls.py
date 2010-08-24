# Create by: Yefe @ 2009-8-17
# Django urls
# $Id$

from django.conf.urls.defaults import patterns, url
from website.apps.account.forgot import views

urlpatterns = patterns('',
    url(r'^$',                  views.index,      name='index'),
    url(r'^(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                                views.confirm,    name='confirm'),
)
