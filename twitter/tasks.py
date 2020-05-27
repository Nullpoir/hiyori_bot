from hiyori_bot.settings.celery import app
from twitter.utils.GenWeatherTweet import GenWeatherTweet
from django.conf import settings
from celery import shared_task
import tweepy
from .markov_chain.markov import Markov

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

    # ツイート送信
    res = api.update_status(tweet)
    print(res)

    return 0

#定時ツイートタスク
@shared_task
def sheduled_tweet():
    # 認証
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AK, AS)
    # コネクション用のインスタンス作成
    api = tweepy.API(auth)

    #ツイート内容作成
    markov = Markov()
    tweet = markov.make_sentence()
    tweet= tweet.strip('[BOS]').strip("\n")

    # ツイート送信
    res = api.update_status(tweet)
    print(res)

#まいこ先生tweet収集
@shared_task
def get_maiko_tweets():
    # 認証
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AK, AS)
    # コネクション用のインスタンス作成
    api = tweepy.API(auth)

    #まいこ先生Tweet取得
    for status in api.user_timeline(id='uma401'):
        # RTとリプライでないものを抽出
        if ((not status.retweeted) and ('RT @' not in status.text)) or (status.in_reply_to_status_id == None):
            print(status.text,status.in_reply_to_status_id)
            continue
        else:
            print("除外tweet")
            print(status.text)
