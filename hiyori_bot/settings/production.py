from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': 'localhost',
        'PORT': '',
        }
    }

#celery task定義
CELERY_BROKER_URL = "redis://127.0.0.1:6379/1"
CELERY_RESULT_BACKEND = "redis://redis:6379"
CELERY_TIMEZONE = 'Asia/Tokyo'
