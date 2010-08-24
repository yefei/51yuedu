import os
import sys

sys.path.append('/home/yefe/website/51yuedu-checkout/src')
os.environ['DJANGO_SETTINGS_MODULE'] = 'website.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
