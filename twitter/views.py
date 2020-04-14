from django.shortcuts import render
from django.views.generic import View
import json
import requests
from django.shortcuts import redirect
from django.http import JsonResponse,HttpResponse,HttpResponseForbidden
import hashlib,hmac,base64
from django.conf import settings
import tweepy
from .markov_chain.markov import Markov
import os
from . import utils

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
        if request.META.get('HTTP_X_TWITTER_WEBHOOKS_SIGNATURE') == None:
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


            state = utils.ClassifyTweet(status['text'])
            if state == "markov":
                # とりあえずマルコフで生成
                markov = Markov()
                tweet = markov.make_sentence()
                tweet= tweet.strip('[BOS]').strip("\n")
            elif state == "weather":
                tweet = utils.GenWeatherTweet("Yokosuka")

            # リプライ送信
            res = api.update_status(
                status=tweet,
                in_reply_to_status_id=status['id'],
                auto_populate_reply_metadata=True
            )
        # フォローされたときの処理
        elif req.get('follow_events') != None:
            id = req['follow_events'][0]['source']['id']
            if id == MY_ID:
                return JsonResponse({"State":"OK"})

            api.create_friendship(id)

        return JsonResponse({"State":"OK"})
