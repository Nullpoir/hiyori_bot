from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hiyori_bot.settings.production")

app = Celery('hiyori_bot',broker='redis://127.0.0.1:6379/1')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registere
app.autodiscover_tasks()
