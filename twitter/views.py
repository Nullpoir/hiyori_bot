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


# Create your views here.

class TwitterEndPointView(View):
    #生存確認とCRC実装
    def get(self, request,*args, **kwargs):
        crc = request.GET.get('crc_token')
        if crc != None:
            validation = hmac.new(
                key=bytes(settings.TWITTER_CONSUMER_SECRET, 'utf-8'),
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
        base = os.path.dirname(os.path.abspath(__file__))
        req = json.loads(request.body)
        # print(req)
        if req.get('tweet_create_events') != None:
            status = req['tweet_create_events'][0]

            #自分へのリプじゃないのと自己リプを弾く
            if (status['in_reply_to_user_id_str'] !=  settings.MY_ID) or (status['user']['id'] == settings.MY_ID):
                print("banned\n","in_reply_to_user_id_str:",status['in_reply_to_user_id_str'],"\nMY_ID:",settings.MY_ID,"\n",status['user']['id'])
                return JsonResponse({"State":"OK"})

            #認証
            auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
            auth.set_access_token(settings.TWITTER_TOKEN, settings.TWITTER_TOKEN_SECRET)
            #コネクション用のインスタンス作成
            api = tweepy.API(auth)
            # print("API CREATE")

            #とりあえずマルコフで生成
            markov = Markov(base+"/markov_chain/model.pyd")
            tweet = markov.make_sentence()
            tweet= tweet.strip('[BOS]').strip("\n")
            #返信
            res = api.update_status(
                status=tweet,
                in_reply_to_status_id=status['id'],
                auto_populate_reply_metadata=True
            )
            print(res)
        elif req.get('follow_events') != None:
            id = req['follow_events'][0]['source']['id']
            if id == settings.MY_ID:
                return JsonResponse({"State":"OK"})
            #認証
            auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
            auth.set_access_token(settings.TWITTER_TOKEN, settings.TWITTER_TOKEN_SECRET)
            #コネクション用のインスタンス作成
            api = tweepy.API(auth)
            api.create_friendship(id)

        return JsonResponse({"State":"OK"})
