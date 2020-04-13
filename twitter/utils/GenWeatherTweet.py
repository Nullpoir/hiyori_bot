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
    abs_zero = 273.15
    #APIに投げるURLを生成
    url = settings.OPENWETHERMAP_URL
    appid = settings.OPENWETHERMAP_API_KEY
    query_url = url + '?q=' + location + '&appid=' + appid

    #APIからJSONをもらう
    weather_dict = requests.get(query_url).json()

    weather = WEATHER[weather_dict['weather'][0]['main']]
    temp = round(weather_dict['main']['temp']-abs_zero,1)
    feel_temp = round(weather_dict['main']['feels_like']-abs_zero,1)
    humidity = weather_dict['main']['humidity']
    wind_speed = weather_dict['wind']['speed']
    wind_direction = DIRECTION[int(weather_dict['wind']['deg']/22.5)]

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
    print(weather == 'Rain')
    if weather == "Rain" or weather == "Snow":
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
        elif (feel_temp >= 25 or feel_temp < 0) and (wind_speed < 4):
             wind_imp = "うう釣りはどうしようかな"
        elif (feel_temp >= 25 or feel_temp > 0) and (wind_speed < 4):
            wind_imp = "でも風は弱いし、小春を誘って釣りに行きたいな・・・"
        else:
            wind_imp = "小春を誘って釣りに行こうかな・・・"

        tweet = report + temp_imp + wind_imp

    return tweet
