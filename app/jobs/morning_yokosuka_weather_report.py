from app.helpers.twitter.push_weather_tweets import push_weather_tweets
import tweepy
from .commons import *

# 毎朝4時に実行させるタスク
def morning_yokosuka_weather_report():
    # ツイート生成
    tweet = push_weather_tweets("Yokosuka")

    # 認証
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AK, AS)

    # コネクション用のインスタンス作成
    api = tweepy.API(auth)

    # ツイート送信
    res = api.update_status(tweet)
    print(res)

    return 0
