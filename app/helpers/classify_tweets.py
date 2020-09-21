import re
from .is_answer_tweet import *

try:
    from ..models import TalkSet
except ImportError:
    pass

try:
    CHECK_DOUBLE_IMPORT_TEXT_SANITIZE
except NameError:
    from .text_sanitize import *
    CHECK_DOUBLE_IMPORT_TEXT_SANITIZE = True

def classify_tweets(text,reply_from_text):
    #テキスト整形
    text = text_sanitize(text)
    # print("sanitized-text:",text)
    pk = is_answer_tweet(reply_from_text)

    if pk > -1:
        if is_correct_answer(pk,text):
            return "問題" + str(pk) + "正解です！"
        else:
            return "問題" + str(pk) + "不正解です・・・"
    else:
        if text == "天気を教えて、ひよりちゃん":
            print()
            return "CMD:weather"
        else:
            return "CMD:others"
