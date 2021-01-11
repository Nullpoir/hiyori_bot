from hiyori_bot.settings.celery import app
from celery import shared_task
from app.jobs import *


def get_tweet_source(status):
    return TWITTER_BASE_URL + status.user.screen_name + "/status/" + status.id_str

# 毎朝4時に実行させるタスク
@shared_task
def morning_yokosuka_weather_report_job():
    morning_yokosuka_weather_report()

# 定時ツイートタスク
@shared_task
def sheduled_tweet_job():
    sheduled_tweet()

# まいこ先生tweet収集
@shared_task
def get_gyokuon_tweets_job():
    get_gyokuon_tweets()


#グッズ情報収集
@shared_task
def get_goodies_tweets():
    get_goodies_tweets()

#自動フォロー解除
@shared_task
def unfollow_task():
    unfollow_task()

#きらファンデイリー遂行確認
@shared_task
def kirafan_daily_notification():
    kirafan_daily_notification()
# クイズ発出
@shared_task
def quiz_publish_job():
    quiz_publish()
