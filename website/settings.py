# Django settings for website project.
import os
ROOT_PATH = os.path.normpath(os.path.dirname(__file__))
PUBLIC_ROOT = os.path.join(ROOT_PATH,'../public/')


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Yefe', 'yefe@ichuzhou.cn'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'mysql',                                   # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '51yuedu',                                     # Or path to database file if using sqlite3.
        'USER': 'root',                                     # Not used with sqlite3.
        'PASSWORD': '',                                 # Not used with sqlite3.
        'HOST': '',                                     # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                     # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

DATE_FORMAT = 'Y-m-d'
TIME_FORMAT = 'a g:i'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '%b%&k9vp6rm(avl)!kl=eze!lx*s2#--aeekre+mz3@ee(ywc8'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PATH,'templates'),
)

ROOT_URLCONF = 'website.urls'

INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.admin',

    'website.apps.account',
    'website.apps.book',
    'website.apps.about',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfMiddleware',
    'django.middleware.locale.LocaleMiddleware',

    'website.apps.account.middleware.AuthenticationMiddleware',
    'website.apps.account.middleware.StatusMiddleware',

    #'django.middleware.cache.FetchFromCacheMiddleware',
)

if DEBUG:
    MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
    MIDDLEWARE_CLASSES.append('website.utils.debug.DebugMiddleware')

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# MySite Config

#MEMCACHEDB = ('222.186.30.7:21202',)
#CACHE_BACKEND = 'locmem://'
#SPHINX_SERVER = '127.0.0.1'

MEMCACHEDB = ('unix:/tmp/memcachedb_51yuedu.sock',)
CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
SPHINX_SERVER = '/home/yefe/app/sphinx-for-chinese/var/searchd.sock'

