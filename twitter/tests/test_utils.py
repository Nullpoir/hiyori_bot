from django.test import TestCase
from twitter.utils import *
from . import datasets
from twitter.models import TalkSet
from core.models import Quiz
# Create your tests here.

class test_utils(TestCase):
    def test_classification(self):
        TalkSet.objects.create(
            name="麦テー",
            trigger_body="MUGI TEA",
            reply="あはははh"
        )
        count = 1
        for t,e in zip(datasets.CLASSIFICATION_TESTS,datasets.CLASSIFICATION_ANSWERS):
            print(count)
            self.assertEqual(ClassifyTweet(t),e)
            count += 1
    def test_ApiConnection(self):
        self.assertNotEqual(ApiConnection("Yokosuka"),"すみません。わかりませんでした・・・")

    def test_GenWeatherTweetText(self):
        for w,a in zip(datasets.WEATHER_TEST_DATAS,datasets.GWTT_CORRECT_ANSWERS):
            t = GenWeatherTweetText(w)
            #print(t)
            self.assertEqual(t,a)
    def test_random_reply(self):
        trigger = "MUGI TEA"
        TalkSet.objects.create(
            name="麦テー",
            trigger_body=trigger,
            reply="あはははh,おほほほh,fjnqwiofn,fwefnioewfnoiw,fwfgiuweb"
        )
        print(ClassifyTweet(trigger))
    def test_is_answer_tweet(self):
        for q,a in zip(datasets.CLASSIFICATION_IS_ANS,datasets.CLASSIFICATION_IS_ANS_ANSWER):
            pk = is_answer_tweet(q)
            self.assertEqual(pk,a)

    def test_is_corrent_answer(self):
        Quiz.objects.create(
            question="おこここここここ",
            answers="あはははh,おほほほh,fjnqwiofn,fwefnioewfnoiw,fwfgiuweb"
        )
        for a,e in zip(datasets.QUIZ_ANSWERS,datasets.QUIZ_ANSWERS_EXPECTED):
            self.assertEqual(is_correct_answer(1,a),e)
