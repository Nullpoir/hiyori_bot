import requests
import os
import json
from django.conf import settings

DIRECTION = [
    '北',
    '北北東',
    '北東',
    '東北東',
    '東',
    '東南東',
    '南東',
    '南南東',
    '南',
    '南南西',
    '南西',
    '西南西',
    '西',
    '西北西',
    '北西',
    '北北西',
]

WEATHER = {
    "Rain":"雨",
    "Clear":"快晴",
    "Clouds":"くもり",
    "Mist":"霧雨",
    "Smoke":"煙霧",
    "Haze":"薄霧",
    "Snow":"雪",
    "Drizzle":"霧雨",
    "Thunderstorm":"雷雨",
    "Squall":"スコール",
    "Tornado":"竜巻",
    "Ash":"火山灰",
    "Fog":"煙霧",
    "Dust":"砂塵",
    "Sand":"砂塵"
}

def GenWeatherTweet(location):
    return GenWeatherTweetText(ApiConnection(location))

def ApiConnection(location):
    abs_zero = 273.15
    #APIに投げるURLを生成
    url = settings.OPENWETHERMAP_URL
    appid = settings.OPENWETHERMAP_API_KEY
    query_url = url + '?q=' + location + '&appid=' + appid

    #APIからJSONをもらう
    response = requests.get(query_url)
    weather_dict = response.json()
    if response.status_code != 200:
        return "すみません。わかりませんでした・・・"

    weather_data = [
        WEATHER[weather_dict['weather'][0]['main']],
        round(weather_dict['main']['temp']-abs_zero,1),
        round(weather_dict['main']['feels_like']-abs_zero,1),
        weather_dict['main']['humidity'],
        weather_dict['wind']['speed'],
        DIRECTION[int(weather_dict['wind']['deg']/22.5)],
    ]
    return weather_data

def GenWeatherTweetText(weather_data):
    weather = weather_data[0]
    temp = weather_data[1]
    feel_temp = weather_data[2]
    humidity = weather_data[3]
    wind_speed = weather_data[4]
    wind_direction = weather_data[5]

    report =str().join([
        'げ、現在の横須賀の天気は'
        ,weather
        ,'で、'+'気温は'
        ,str(temp)
        ,'℃で体感温度は'
        ,str(feel_temp)
        ,'℃です・・・\n'
        , '風は風速'
        ,str(wind_speed)
        ,'mで'
        ,wind_direction
        ,'から吹いてきます・・・\n'
    ])
    temp_imp = ""
    wind_imp = ""
    if weather == "雨" or weather == "雪":
        tweet = report + "今日の釣りはいいかな・・・"
    else:
        if feel_temp < 25 and feel_temp >= 10:
            temp_imp = "今日は暖かいですね、"
        elif feel_temp >= 25:
            temp_imp = "今日は暑いですね・・・"
        elif feel_temp < 10:
            temp_imp = "今日は寒いですね・・・"

        if wind_speed > 4:
            wind_imp = "ただ風が強いから釣りは難しそう"
        elif (feel_temp >= 30 or feel_temp < 0) and (wind_speed < 4):
             wind_imp = "うう釣りはどうしようかな"
        elif (feel_temp < 10 and feel_temp > 0) and (wind_speed < 4):
            wind_imp = "でも風は弱いし、小春を誘って釣りに行きたいな・・・"
        elif (feel_temp < 30 and feel_temp >= 25) and (wind_speed < 4):
            wind_imp = "でも風は弱いし、小春を誘って釣りに行きたいな・・・"
        else:
            wind_imp = "小春を誘って釣りに行こうかな・・・"

        tweet = report + temp_imp + wind_imp

    return tweet
