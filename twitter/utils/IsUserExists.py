from core.models import User

def is_twitter_user_exists(twitter_id):
    try:
        user = User.objects.get(twitter_id=str(id))
    except:
        user = None
    if user == None:
        return False
    else:
        return True
