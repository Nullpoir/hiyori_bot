import re
from twitter.models import TalkSet
from twitter.TextSanitize import TextSanitize
import random
from .IsAnswerTweet import *

def ClassifyTweet(text,reply_from_text):
    #テキスト整形
    text = TextSanitize(text)
    # print("sanitized-text:",text)
    pk = is_answer_tweet(reply_from_text)

    if pk > -1:
        if is_correct_answer(pk,text):
            return "問題" + str(pk) + "正解です！"
        else:
            return "問題" + str(pk) + "不正解です・・・"
    else:
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
