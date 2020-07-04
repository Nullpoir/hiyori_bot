from django.db import models

class User(models.Medel):
    # 共通
    # twitter関連
    twitter_id = models.CharField(vervose_name="Twitterスクリーンネーム")