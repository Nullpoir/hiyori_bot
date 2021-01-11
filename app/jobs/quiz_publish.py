import tweepy
import random
from app.models import Quiz
from .commons import *

# クイズ発出
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
