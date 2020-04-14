from django.test import TestCase
from twitter.utils import *
from . import datasets
# Create your tests here.

class test_utils(TestCase):
    def test_classification(self):

        expect_returns = [
            "markov",
            "weather",
            "markov",
            "weather",
        ]
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
