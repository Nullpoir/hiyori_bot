import tweepy
from app.models import User
from .commons import *

# フォロー解除タスク
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
            api.destroy_friendship(i)
            user = User.objects.get(twitter_id=str(i))
            user.is_active = False
            user.save()
