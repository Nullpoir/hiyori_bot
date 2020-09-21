from django.test import TestCase
from app.models import *
import random

class test_quiz(TestCase):
    def test_create_quiz(self):
        Quiz.objects.create(
            question="おこここここここ",
            answers="あはははh,おほほほh,fjnqwiofn,fwefnioewfnoiw,fwfgiuweb"
        )
    def test_quiz_shuffle(self):
        for i in range(10):
            Quiz.objects.create(
            question="おこここここここ" + str(i),
            answers="あはははh,おほほほh,fjnqwiofn,fwefnioewfnoiw,fwfgiuweb"
        )
        count = Quiz.objects.all().count()
        query_set = Quiz.objects.all()
        random_list = []
        for i in range(count):
            random_list.append(i)

        random.shuffle(random_list)

        for i in random_list:
            tweet = '問題' + str(query_set[i].pk) + '\n' + query_set[i].question
            try:
                print(tweet)
                break
            except:
                continue
