from app.helpers import *

#テキスト分類課題用テストデータ
CLASSIFICATION_TESTS = [
"""@mHiyori0104
今日の天気は？""",
"""@mHiyori0104
天気を教えて、ひよりちゃん""",
"""@mHiyori0104
天気を教えて、ひよりちゃん？""",
"""@mHiyori0104
天気を教えて、ひよりちゃん?""",
"""@mHiyori0104
天気を教えて、ひよりちゃん



""",
"""@mHiyori0104
MUGI TEA
""",
"""@mHiyori0104
MUGITEA


""",
"""@mHiyori0104
「MUGITEA」


""",
"""@mHiyori0104
「MUGITEA


""",
"""@mHiyori0104
MUGITEA」


""",
]
#テキスト分類課題用正解データ
CLASSIFICATION_ANSWERS = [
    "CMD:others",
    "CMD:weather",
    "CMD:weather",
    "CMD:weather",
    "CMD:weather",
    "あはははh",
    "あはははh",
]
#天気テキスト生成テストデータ
WEATHER_TEST_DATAS = [
    [
        WEATHER["Rain"],
        18.1,
        10.1,
        80,
        1,
        DIRECTION[15]
    ],
    [
        WEATHER["Clear"],
        18.1,
        10.1,
        80,
        1,
        DIRECTION[15]
    ],
    [
        WEATHER["Clear"],
        18.1,
        10.1,
        80,
        5,
        DIRECTION[15]
    ],
    [
        WEATHER["Clear"],
        26,
        31,
        80,
        5,
        DIRECTION[15]
    ],
    [
        WEATHER["Clear"],
        31,
        31,
        80,
        3,
        DIRECTION[15]
    ],
]

#天気テキスト生成正解データ
GWTT_CORRECT_ANSWERS = [
"""げ、現在の横須賀の天気は雨で、気温は18.1℃で体感温度は10.1℃です・・・
風は風速1mで北北西から吹いてきます・・・
今日の釣りはいいかな・・・""",
"""げ、現在の横須賀の天気は快晴で、気温は18.1℃で体感温度は10.1℃です・・・
風は風速1mで北北西から吹いてきます・・・
今日は暖かいですね、小春を誘って釣りに行こうかな・・・""",
"""げ、現在の横須賀の天気は快晴で、気温は18.1℃で体感温度は10.1℃です・・・
風は風速5mで北北西から吹いてきます・・・
今日は暖かいですね、ただ風が強いから釣りは難しそう""",
"""げ、現在の横須賀の天気は快晴で、気温は26℃で体感温度は31℃です・・・
風は風速5mで北北西から吹いてきます・・・
今日は暑いですね・・・ただ風が強いから釣りは難しそう""",
"""げ、現在の横須賀の天気は快晴で、気温は31℃で体感温度は31℃です・・・
風は風速3mで北北西から吹いてきます・・・
今日は暑いですね・・・うう釣りはどうしようかな""",
]
#クイズ用のリプか判定課題
CLASSIFICATION_IS_ANS = [
"""問題1
ここここここ
こここここここ""",
"""問題2
Jul 05 20:35:31 os3-360-13067 gunicorn[3105]: 空白を埋める問題です
Jul 05 20:35:31 os3-360-13067 gunicorn[3105]: ウサギの王子様〇〇〇〇へいくの〇〇〇〇に入る言葉は？""",
"""ここここここ
こここここここ""",
"""問題4
ここここここ
こここここここ""",
None
]

#クイズ用のリプか判定課題の正解
CLASSIFICATION_IS_ANS_ANSWER = [
    1,2,-1,4,-1
]

#クイズ入力
QUIZ_ANSWERS = [
    "あはははh\n",
    "あはははh？",
    "あはははh?\n",
    "あはははh」\n",
    "おほほほh",
    "おほほほhaaaaaaa",
]
#正当判定期待値
QUIZ_ANSWERS_EXPECTED = [
    True,
    True,
    True,
    True,
    True,
    False,
]
