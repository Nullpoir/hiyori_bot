from django.test import TestCase
from app.helpers import *
from . import datasets
from app.models import *
# Create your tests here.

class test_helpers(TestCase):
    def test_classification(self):
        TalkSet.objects.create(
            name="麦テー",
            trigger_body="MUGI TEA",
            reply="あはははh"
        )
        count = 1
        for t,e in zip(datasets.CLASSIFICATION_TESTS,datasets.CLASSIFICATION_ANSWERS):
            print(count)
            if classify_tweets(t,None) == 'CMD:others':
                talksets = TalkSet.objects.all()
                for ts in talksets:
                    if t == ts.trigger:
                        replies = ts.reply.split(',')
                        index_length = len(replies) - 1
                        key = random.randint(0,index_length)
                        self.assertEqual(replies[key],e)
            else:
                self.assertEqual(classify_tweets(t,None),e)
            count += 1
    def test_get_info_from_api(self):
        self.assertNotEqual(get_info_from_api("Yokosuka"),"すみません。わかりませんでした・・・")

    def test_get_weather_info(self):
        for w,a in zip(datasets.WEATHER_TEST_DATAS,datasets.GWTT_CORRECT_ANSWERS):
            t = get_weather_info(w)
            #print(t)
            self.assertEqual(t,a)
    def test_random_reply(self):
        trigger = "MUGI TEA"
        TalkSet.objects.create(
            name="麦テー",
            trigger_body=trigger,
            reply="あはははh,おほほほh,fjnqwiofn,fwefnioewfnoiw,fwfgiuweb"
        )
        print(classify_tweets(trigger,''))
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
