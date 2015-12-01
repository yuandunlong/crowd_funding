import  hashlib

from flask import  request,Blueprint,Response

beecloud_api=Blueprint("beecloud_api",__name__)
@beecloud_api.route("/private/beecloud/callback")
def callback():
    data=request.json
    appid = ''
    appsecret = ''
    timestamp = data['timestamp']
    sign = data['sign']
    thissign = hashlib.md5(appid+appsecret+str(timestamp))
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