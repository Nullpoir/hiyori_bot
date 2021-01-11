import tweepy
from app.shared.markov import Markov
from .commons import *

# 定時ツイートタスク
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
        except TweepyError as e:
            if e.get("message") == "Status is a duplicate.":
                res = api.update_status(tweet)
    print(res)

