from hiyori_bot.settings.celery import app
from twitter.utils.GenWeatherTweet import GenWeatherTweet
from django.conf import settings
from celery import shared_task
import tweepy

CK = settings.TWITTER_CONSUMER_KEY
CS = settings.TWITTER_CONSUMER_SECRET
AK = settings.TWITTER_TOKEN
AS = settings.TWITTER_TOKEN_SECRET

#毎朝4時に実行させるタスク
@shared_task
def morning_yokosuka_weather_report():
    tweet = GenWeatherTweet("Yokosuka")

    # 認証
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AK, AS)
    # コネクション用のインスタンス作成
    api = tweepy.API(auth)

    # 定期ツイート送信
    res = api.update_status(tweet)
    print(res)

    return 0
