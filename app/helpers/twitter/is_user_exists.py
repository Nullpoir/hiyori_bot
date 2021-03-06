from app.models import User

def is_twitter_user_exists(twitter_id):
    if not (type(twitter_id) is str):
        twitter_id = str(twitter_id)
    try:
        user = User.objects.get(twitter_id=twitter_id)
    except:
        user = None
    if user is None:
        return False
    else:
        return True
