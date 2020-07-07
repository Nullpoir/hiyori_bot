from hiyori_bot.settings.celery import app
from django.conf import settings
from celery import shared_task
import random
import tweepy
from core.models import Quiz

CK = settings.TWITTER_CONSUMER_KEY
CS = settings.TWITTER_CONSUMER_SECRET
AK = settings.TWITTER_TOKEN
AS = settings.TWITTER_TOKEN_SECRET

@shared_task
def quiz_publish():
    # 認証
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AK, AS)

    # コネクション用のインスタンス作成
    api = tweepy.API(auth)

    count = Quiz.objects.all().count()
    query_set = Quiz.objects.all()
    random_list = []
    for i in range(count):
        random_list.append(i)

    random.shuffle(random_list)

    for i in random_list:
        tweet = '問題' + str(query_set[i].pk) + '\n' + query_set[i].question + '\n' + '#ひよちの可愛いクイズ'
        try:
            api.update_status(tweet)
            break
        except:
            continue
