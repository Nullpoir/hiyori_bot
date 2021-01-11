import tweepy
from app.models import User
from .commons import *

#きらファンデイリー遂行確認
def kirafan_daily_notification():
    # 認証
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AK, AS)
    # コネクション用のインスタンス作成
    api = tweepy.API(auth)

    for i in User.objects.all().filter(is_active=True,is_daily=True)[:80]:
        screen_name = '@' + i.twitter_screen_name()
        tweet = screen_name + '\n' + 'あ、あの！きらファンデイリー遂行確認のお時間です・・・'
        try:
            res = api.update_status(tweet)
            print('send to' + screen_name)
        except:
            pass
