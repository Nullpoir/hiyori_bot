import tweepy
import datetime
from discordwebhook import Discord
from .commons import *

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

