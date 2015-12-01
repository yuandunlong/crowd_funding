#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-09-18 10:04:17
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-11-18 17:50:38
# -*- coding: utf-8 -*-
import  hashlib

from flask import  request,Blueprint,Response,current_app

beecloud_api=Blueprint("beecloud_api",__name__)
@beecloud_api.route("/private/beecloud/callback",methods=["POST"])
def callback():
    data=request.json
    appid = current_app.config.get("BEECLOUD_APP_ID")
    appsecret = current_app.config.get("BEECLOUD_APP_SECRET")
    print appsecret,appid
    timestamp = data['timestamp']
    sign = data['sign']
    thissign = hashlib.md5(appid+appsecret+str(timestamp))
    print thissign,sign
    # 验证签名
    if thissign == sign:
        # 处理业务逻辑
        channel_type = data['channelType']
        transaction_type = data['transactionType']
        trade_success = data['tradeSuccess']
        message_detail = data['messageDetail']

        return Response('success')

    else:
        return Response("fail")