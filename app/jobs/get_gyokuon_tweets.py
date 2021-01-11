import tweepy
import datetime
from discordwebhook import Discord
from .commons import *

# まいこ先生tweet収集
def get_gyokuon_tweets():
    # 認証
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AK, AS)
    # コネクション用のインスタンス作成
    api = tweepy.API(auth)

    #クエリ生成
    uchino_id = 'uma401'
    anime_official_id = 'slowloop_tv'
    since = datetime.datetime.utcnow() - datetime.timedelta(minutes=1)
    query = f'from:{anime_official_id} OR from:{uchino_id} -filter:retweets since:{since.strftime("%Y-%m-%d_%H:%M:%S_UTC")}'

    #Discord WebHook接続
    discord = Discord(url=DISCORD_WEBHOOK_URL_MAIKO)
    #まいこ先生Tweet取得
    for status in api.search(q=query):
        #自己リプとリプじゃ無いツイートは許可
        if (f'@{uchino_id}' in status.text) or (f'@{anime_official_id}' in status.text) or ( not('@' in status.text)):
            #文章生成
            discord_post_text = get_tweet_source(status)
            print(discord_post_text)
            # Discordに投げる
            discord.post(content=discord_post_text)
        else:
            #何もしない
            pass
