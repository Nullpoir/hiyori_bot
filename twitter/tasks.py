from hiyori_bot.settings.celery import app
from twitter.utils.GenWeatherTweet import GenWeatherTweet
from django.conf import settings
from celery import shared_task
import tweepy
from .markov_chain.markov import Markov
import datetime
from discordwebhook import Discord
from core.models import User

TWITTER_BASE_URL = "https://twitter.com/"
CK = settings.TWITTER_CONSUMER_KEY
CS = settings.TWITTER_CONSUMER_SECRET
AK = settings.TWITTER_TOKEN
AS = settings.TWITTER_TOKEN_SECRET
MY_ID = settings.MY_ID
DISCORD_WEBHOOK_URL_MAIKO = settings.DISCORD_WEBHOOK_URL_MAIKO
DISCORD_WEBHOOK_URL_GOODIES = settings.DISCORD_WEBHOOK_URL_GOODIES
SCREEN_NAME = 'mHiyori0324'

def get_tweet_source(status):
    return TWITTER_BASE_URL + status.user.screen_name + "/status/" + status.id_str

# 毎朝4時に実行させるタスク
@shared_task
def morning_yokosuka_weather_report():
    # ツイート生成
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

# 定時ツイートタスク
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
    is_end = False
    while not is_end:
        try:
            res = api.update_status(tweet)
            is_end = True
        except TweepError as e:
            if e.get("message") == "Status is a duplicate.":
                res = api.update_status(tweet)
    print(res)

# まいこ先生tweet収集
@shared_task
def get_maiko_tweets():
    # 認証
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AK, AS)
    # コネクション用のインスタンス作成
    api = tweepy.API(auth)

    #クエリ生成
    id='uma401'
    since = datetime.datetime.utcnow() - datetime.timedelta(minutes=1)
    query = "from:" + id + " -filter:retweets since:" + since.strftime("%Y-%m-%d_%H:%M:%S_UTC")


    #Discord WebHook接続
    discord = Discord(url=DISCORD_WEBHOOK_URL_MAIKO)
    #まいこ先生Tweet取得
    for status in api.search(q=query):
        #自己リプとリプじゃ無いツイートは許可
        print(('@' + id) in status.text) or ( not('@' in status.text))
        if (('@' + id) in status.text) or ( not('@' in status.text)):
            #文章生成
            discord_post_text = get_tweet_source(status)
            print(discord_post_text)
            # Discordに投げる
            discord.post(content=discord_post_text)
        else:
            #何もしない
            pass


#グッズ情報収集
@shared_task
def get_goodies_tweets():
    # 認証
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AK, AS)
    # コネクション用のインスタンス作成
    api = tweepy.API(auth)

    #クエリ生成
    list ='list:1266373880949510144'
    since = datetime.datetime.utcnow() - datetime.timedelta(minutes=1)
    query = "\"スローループ\" "+ list + " -filter:retweets -filter:replies since:" + since.strftime("%Y-%m-%d_%H:%M:%S_UTC")

    # Discord WebHook接続
    discord = Discord(url=DISCORD_WEBHOOK_URL_GOODIES)
    # まいこ先生Tweet取得
    for status in api.search(q=query):
        #文章生成
        discord_post_text = get_tweet_source(status)
        print(discord_post_text)
        # Discordに投げる
        discord.post(content=discord_post_text)
        # RTする
        api.retweet(status.id)

#自動フォロー解除
@shared_task
def unfollow_task():
    # 認証
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AK, AS)
    # コネクション用のインスタンス作成
    api = tweepy.API(auth)

    followers = api.followers_ids(SCREEN_NAME)
    friends = api.friends_ids(SCREEN_NAME)

    for i in friends:
        if i not in followers:
            user = User.objects.get(twitter_id=str(i))
            user.is_active = False
            user.save()
            api.destroy_friendship(i)

