import re
from twitter.models import TalkSet

def ClassifyTweet(text):
    text = re.sub(r'@mHiyori0324', "", text)
    text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
    text=re.sub('\n', "", text)
    text=re.sub(' ', "", text)
    text=re.sub('　', "", text)
    talksets = TalkSet.objects.all()
    for t in talksets:
        print(t.trigger,text)
        if text == t.trigger:
            return t.reply

    if text.strip("？").strip("?") == "天気を教えて、ひよりちゃん":
        return "CMD:weather"
    else:
        return "CMD:markov"
