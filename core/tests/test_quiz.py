from django.test import TestCase
from core.models import *

class test_quiz(TestCase):
    def test_create_quiz(self):
        Quiz.objects.create(
            question="おこここここここ",
            answers="あはははh,おほほほh,fjnqwiofn,fwefnioewfnoiw,fwfgiuweb"
        )