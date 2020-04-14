from .base import *
# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DEBUG = True

TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
TWITTER_TOKEN = os.environ.get('TWITTER_TOKEN')
TWITTER_TOKEN_SECRET = os.environ.get('TWITTER_TOKEN_SECRET')

OPENWETHERMAP_API_KEY = os.environ.get('OPENWETHERMAP_API_KEY')
OPENWETHERMAP_URL = os.environ.get('OPENWETHERMAP_URL')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
