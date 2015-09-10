#-*- coding: UTF-8 -*-  

from third.CCPRestSDK import REST
import ConfigParser

#主帐号
accountSid= '8a48b5514ebe1674014ecd5617870f46';

#主帐号Token
accountToken= '78e0086b5382483896991e1031a5c874';

#应用Id
appId='aaf98f894edd4c1e014edfb9e6210466';

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com';

#请求端口 
serverPort='8883';

#REST版本号
softVersion='2013-12-26';

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id

def sendTemplateSMS(to,datas,tempId):

    
    #初始化REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    ret='1111'
    result = rest.sendTemplateSMS(to,datas,tempId)
    for k,v in result.iteritems(): 
        
        if k=='templateSMS' :
                for k,s in v.iteritems(): 
                    print '%s:%s====' % (k, s)
        else:
            print '%s:%s+++' % (k, v)
        if k=='statusCode':
          ret=v
    return ret
    
   
#sendTemplateSMS(手机号码,内容数据,模板Id)


