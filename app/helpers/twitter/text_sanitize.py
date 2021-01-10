"""
整形のルール
@mHiyori0104を消す
リンクを消す
改行を消す
?と？と「と」を消す
全角半角両方のスペースを消す
"""
import re

def text_sanitize(text):
    #テキスト整形
    text = re.sub(r'@mHiyori0104', "", text)
    text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
    text = re.sub('\n', "", text)
    text = re.sub(' ', "", text)
    text = re.sub('　', "", text)
    text = re.sub('\?', "", text)
    text = re.sub('\？', "", text)
    text = re.sub('「', "", text)
    text = re.sub('｢', "", text)
    text = re.sub('」', "", text)
    text = re.sub('｣', "", text)

    return text
