import re
from twitter.models import TalkSet
from twitter.TextSanitize import TextSanitize
import random

def ClassifyTweet(text):
    #テキスト整形
    text = TextSanitize(text)
    print("sanitized-text:",text)
    talksets = TalkSet.objects.all()
    for t in talksets:
        if text == t.trigger:
            replies = t.reply.split(',')
            index_length = len(replies) - 1
            key = random.randint(0,index_length)
            return replies[key]
    if text == "天気を教えて、ひよりちゃん":
        print()
        return "CMD:weather"
    else:
        return "CMD:markov"
