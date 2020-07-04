from django.db import models
import tweepy
from datetime import datetime
from django.utils import timezone
from django.conf import settings

CK = settings.TWITTER_CONSUMER_KEY
CS = settings.TWITTER_CONSUMER_SECRET
AK = settings.TWITTER_TOKEN
AS = settings.TWITTER_TOKEN_SECRET
MY_ID = settings.MY_ID

class User(models.Model):
    # 共通
    created_at = models.DateTimeField(
        verbose_name='作成日',
        default=datetime.now
    )
    update_at = models.DateTimeField(
        verbose_name='更新日',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        verbose_name='有効',
        default=True
    )
    # twitter関連
    twitter_id = models.CharField(
        verbose_name="Twitterスクリーンネーム",
        max_length=22,
        unique=True
    )

    def save(self):
        # 更新がある度に更新日を変更
        update_at = datetime.now
        super(User, self).save()
    def twitter_screen_name(self):
         # 認証
        auth = tweepy.OAuthHandler(CK, CS)
        auth.set_access_token(AK, AS)
        # コネクション用のインスタンス作成
        api = tweepy.API(auth)
        # データ取得
        user = api.get_user(self.twitter_id)

        return user['screen_name']

    def twitter_name(self):
         # 認証
        auth = tweepy.OAuthHandler(CK, CS)
        auth.set_access_token(AK, AS)
        # コネクション用のインスタンス作成
        api = tweepy.API(auth)
        # データ取得
        user = api.get_user(self.twitter_id)

        return user['name']
