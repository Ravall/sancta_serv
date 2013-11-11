# -*- coding: utf-8 -*-
from control_dj.settings import *
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'sancta_serv',
            'USER': 'sancta_serv_user',
            'PASSWORD': 'sancta_serv_user_password',
            'HOST': '127.0.0.1',
            'PORT': '',
        }
    }
else:
    from production import DATABASES

API_URL = 'http://api.sancta.local' if not DEBUG else 'http://api.sancta.ru'

ALLOWED_HOSTS = ['sancta.ru', '127.0.0.1']


INSTALLED_APPS += (
    'numerology',
    'biorythms',
    'raven.contrib.django.raven_compat',
    'pytils',
    'support',
    'django.contrib.humanize'
)
MIDDLEWARE_CLASSES += (
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
)

SECRET_KEY = '#xrq3fac1=ehd2sh0$18&oy(da7@ae=d+8hox3v+t$4*g6d)u9'
ROOT_URLCONF = 'serv.urls'
WSGI_APPLICATION = 'serv.wsgi.application'


CACHE_API_TIMEOUT = 60*60*24*3
CACHE_API_TIMEOUT_FAST = 60*1


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/home/var/cache/' if not DEBUG else '/tmp/cache'
    },
}

FAVICON_PATH = STATIC_URL + 'img/favicon.ico'

RAVEN_CONFIG = {
    'dsn': 'http://5ff6cd1e2a4240d4bb99785cb5ff6484:f8ad63d16b37493d94a713d968ede772@sentry.sancta.ru/4',
}

