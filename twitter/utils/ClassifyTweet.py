import re
from twitter.models import TalkSet

def ClassifyTweet(text):
    talksets = TalkSet.objects.all()
    for t in talksets:
        print(t.trigger,text.strip("@mHiyori0324").strip(" ").strip("　").strip("\n"))
        if text.strip("@mHiyori0324").strip(" ").strip("　").strip("\n") == t.trigger:
            return t.reply

    if text.strip("@mHiyori0324").strip(" ").strip("　").strip("\n").strip("？").strip("?") == "天気を教えて、ひよりちゃん":
        return "CMD:weather"
    else:
        return "CMD:markov"
