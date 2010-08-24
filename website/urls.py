from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the docs:
#from django.contrib import docs

# Uncomment the next two lines to enable the admin:
from django.contrib import admin, ajax
admin.autodiscover()
ajax.autodiscover()

from website.settings import PUBLIC_ROOT
from website.utils import captcha

urlpatterns = patterns('',
    (r'^public/(?P<path>.*)$', 'django.views.static.serve', {'document_root':PUBLIC_ROOT, 'show_indexes':True}),
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template':'index.html'}),
    url(r'^captcha.png$', captcha.make, name='captcha'),
    
    (r'^my/',       include('website.apps.account.urls',     'account')),
    (r'^book/',     include('website.apps.book.urls',     'book')),
    (r'^search/',     include('website.apps.search.urls',     'search')),
    (r'^about/',     include('website.apps.about.urls',     'about')),
    
    (r'^\$',        include(ajax.urls)),
    (r'^_admin/',   include(admin.site.urls)),
)
