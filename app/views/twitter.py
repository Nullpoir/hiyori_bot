from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect
from django.http import JsonResponse,HttpResponse,HttpResponseForbidden
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json
import requests
import os
import hashlib,hmac,base64
import tweepy
from app.markov.markov import Markov
from app import helpers
from app.models import *

CK = settings.TWITTER_CONSUMER_KEY
CS = settings.TWITTER_CONSUMER_SECRET
AK = settings.TWITTER_TOKEN
AS = settings.TWITTER_TOKEN_SECRET
MY_ID = settings.MY_ID

class TwitterEndPointView(View):
    # 生存確認とCRC実装
    def get(self, request,*args, **kwargs):
        crc = request.GET.get('crc_token')
        if crc != None:
            validation = hmac.new(
                key=bytes(CS, 'utf-8'),
                msg=bytes(crc, 'utf-8'),
                digestmod=hashlib.sha256
            )
            digested = base64.b64encode(validation.digest())
            return JsonResponse(
                {'response_token': 'sha256=' + format(str(digested)[2:-1])}
            )
        else:
            return JsonResponse({"State":"Alive!"})

    #実際のリクエスト処理
    def post(self, request, *args, **kwargs):
        #入力検証
        validation = hmac.new(
            key=bytes(CS, 'utf-8'),
            msg=bytes(request.body),
            digestmod=hashlib.sha256
        )
        # リクエストヘッダなしを弾く
        if request.META.get('HTTP_X_TWITTER_WEBHOOKS_SIGNATURE') is None:
            return HttpResponseForbidden()

        #検証データ作成
        signature = request.META.get('HTTP_X_TWITTER_WEBHOOKS_SIGNATURE')[7:].encode('utf-8')
        digested = base64.b64encode(validation.digest())

        #おかしな検証結果になったら弾く
        if not hmac.compare_digest(signature,digested):
            return HttpResponseForbidden()

        req = json.loads(request.body)
        # 認証
        auth = tweepy.OAuthHandler(CK, CS)
        auth.set_access_token(AK, AS)
        # コネクション用のインスタンス作成
        api = tweepy.API(auth)
        # print(req)
        # リプライが来たときの処理
        if req.get('tweet_create_events') != None:
            status = req['tweet_create_events'][0]
            # 自分へのリプじゃないのと自己リプを弾く
            if (status['in_reply_to_user_id_str'] !=  MY_ID) or (status['user']['id'] == MY_ID):
                return JsonResponse({"State":"OK"})

            print(status['text'])
            try:
                reply_from_text = api.get_status(status['in_reply_to_status_id']).text
            except:
                reply_from_text = None

            state = helpers.classify_tweets(status['text'],reply_from_text)
            if state == "CMD:markov":
                talksets = TalkSet.objects.all()
                for t in talksets:
                    if state == t.trigger:
                        replies = t.reply.split(',')
                        index_length = len(replies) - 1
                        key = random.randint(0,index_length)
                        tweet = replies[key]
                        res = api.update_status(
                            status=tweet,
                            in_reply_to_status_id=status['id'],
                            auto_populate_reply_metadata=True
                        )
                        return JsonResponse({"State":"OK"})
                # とりあえずマルコフで生成
                markov = Markov()
                tweet = markov.make_sentence()
                tweet= tweet.strip('[BOS]').strip("\n")
            elif state == "CMD:weather":
                tweet = helpers.push_weather_tweets("Yokosuka")
            else:
                tweet = state

            # リプライ送信
            res = api.update_status(
                status=tweet,
                in_reply_to_status_id=status['id'],
                auto_populate_reply_metadata=True
            )
        # フォローされたときの処理
        elif req.get('follow_events') != None:
            if(req['follow_events'][0]['type'] == "follow"):
                id = req['follow_events'][0]['source']['id']
                if id == MY_ID:
                    return JsonResponse({"State":"OK"})
                if helpers.is_twitter_user_exists(id):
                    user = User.objects.get(twitter_id=str(id))
                    user.is_active = True
                    user.save()
                else:
                    # user登録
                    user = User(twitter_id=str(id))
                    user.save()
                # フォロー
                api.create_friendship(id)

        elif req.get('direct_message_events') != None:

            sender_id = req['direct_message_events'][0]['message_create']['sender_id']
            user_id = req['direct_message_events'][0]['message_create']['target']['recipient_id']
            message =  req['direct_message_events'][0]['message_create']['message_data']['text']
            if sender_id == MY_ID:
                return JsonResponse({"State":"OK"})
            if helpers.is_twitter_user_exists(sender_id):
                # DM送信
                user = User.objects.get(twitter_id=str(sender_id))
                if user.is_active:
                    cmd = helpers.classify_direct_message(message)
                    if cmd == 'CMD:DAILY':
                        if user.is_daily:
                            reply = "わかりました。きらファンデイリーの通知をやめますね..."
                        else:
                            reply = "わかりました。きらファンデイリーの通知を毎日23時半にします。"

                        user.is_daily = not user.is_daily
                        user.save()
                        api.send_direct_message(sender_id,reply)
                    elif cmd is None:
                        api.send_direct_message(sender_id,"すみませんよくわかりませんでした。")


        return JsonResponse({"State":"OK"})

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(TwitterEndPointView, self).dispatch(request, *args, **kwargs)
