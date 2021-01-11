from django.conf import settings

# 共通で利用する変数
TWITTER_BASE_URL = "https://twitter.com/"
CK = settings.TWITTER_CONSUMER_KEY
CS = settings.TWITTER_CONSUMER_SECRET
AK = settings.TWITTER_TOKEN
AS = settings.TWITTER_TOKEN_SECRET
MY_ID = settings.MY_ID
DISCORD_WEBHOOK_URL_MAIKO = settings.DISCORD_WEBHOOK_URL_MAIKO
DISCORD_WEBHOOK_URL_GOODIES = settings.DISCORD_WEBHOOK_URL_GOODIES
SCREEN_NAME = 'mHiyori0104'


def get_tweet_source(status):
    return TWITTER_BASE_URL + status.user.screen_name + "/status/" + status.id_str
