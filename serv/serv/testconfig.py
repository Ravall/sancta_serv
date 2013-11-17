# -*- coding: utf-8 -*-
import os
IS_TESTING = 1
from settings import SECRET_KEY, SITE_ID, STATIC_URL, ROOT_URLCONF
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sancta_serv_test',
        'USER': 'sancta_serv_user',
        'PASSWORD': 'sancta_serv_user_password',
        'HOST': '127.0.0.1',
        'PORT': '',
        'TEST_DEPENDENCIES': []
    }
}
# приложения, которые нужно тестировать
INSTALLED_APPS = (
    'serv',
    'support'
)
