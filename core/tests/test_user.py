from django.test import TestCase
from core.models import *

class test_user(TestCase):
    def test_create_user(self):
        User.objects.create(twitter_id="111111111")
        User.objects.create(twitter_id="111111112")