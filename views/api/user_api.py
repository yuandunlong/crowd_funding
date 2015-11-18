#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-09-10 22:16:29
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-11-18 19:59:27
from flask import request, Blueprint,json,Response,current_app
from utils.decorator import json_response,require_token
from database.models import Token,User,db,Attention,Project,ArtistProfile
from services import user_service
from hashlib import md5
from werkzeug.contrib.cache import SimpleCache
from utils.sms import sendTemplateSMS
from utils import stringutil,result_set_convert
user_api=Blueprint("user_api",__name__ )
sms_code_cache = SimpleCache(threshold=5000, default_timeout=300)
@user_api.route("/private/user/get_challenge",methods=['POST'])
@json_response
def get_challenge(result):
    data=request.get_json()
    account=data['account']
    result['challenge']=user_service.get_challenge()
    
@user_api.route('/private/user/get_access_token',methods=['POST'])
@json_response
def get_access_token(result):
    data=request.get_json()
    challenge=data['challenge']
    account=data['mobile']
    pass_code=data['pass_code']
    user=User.query.filter_by(mobile=account).first()
    if not user:
        result['code']=1
        result['msg']="mobile is not exist"
        return 
    m=md5()
    m.update(user.passwd+challenge)
    check_code=m.hexdigest()
    check_code=check_code.upper()
    pass_code=pass_code.upper()

    print "check_code:=",check_code,"pass_code:=",pass_code
    if check_code!=pass_code:
        result['code']=1
        result['msg']="password is not correct"
        return
    token=Token.query.filter_by(user_id=user.id).first()
    if token:
        access_token=token.token
    else:
        access_token=user_service.get_access_token()
        token=Token(challenge=challenge,user_id=user.id,token=access_token,expires=-1)
        db.session.add(token)
        db.session.commit()
    result['access_token']=access_token
    result['expires']=-1
@user_api.route('/public/user/send_sms_code',methods=['GET'])
@json_response
def send_sms_code(result):

    mobile=request.args.get('mobile')

    if not mobile or mobile=='':
        result['code']=1
        result['msg']='mobile is empty'
        return 
    user=User.query.filter_by(mobile=mobile).first()
    if user:
        result['code']=1
        result['msg']='手机号码已经存在'
        return 
    sms_code=stringutil.random_digits(6)
    (status_code,smsResult)=sendTemplateSMS(mobile,[sms_code,'5'],1)
    if smsResult:
        current_app.logger.info(smsResult)
    if status_code=='000000':
        sms_code_cache.set(mobile,sms_code)
        print 'sms_code',sms_code
        return
    else:
        result['code']=1
        result['msg']='验证码发送失败，请稍后再试'

@user_api.route('/public/user/sign_up',methods=['POST'])
@json_response
def sign_up(result):
    data=request.get_json()
    mobile=data['mobile']
    passwd=data['pwd']
    sms_code=data['sms_code']
    user=User.query.filter_by(mobile=mobile).first()
    if user:
        result['code']=1
        result['msg']='手机号码已经存在'
        return 
    else:
        if sms_code==sms_code_cache.get(mobile):
            user=User(mobile=mobile,passwd=passwd)
            db.session.add(user)
            db.session.commit()
            access_token=user_service.get_access_token()
            token=Token(challenge=user_service.get_access_token(),user_id=user.id,token=access_token,expires=-1)
            db.session.add(token)
            db.session.commit()
            result['access_token']=access_token
            result['expires']=-1
        else:
            result['code']=1
            result['msg']='验证码不正确'

@user_api.route('/private/user/get_user_info',methods=['POST'])
@require_token
@json_response
def get_user_info(result,user):
    ret=user.as_map()
    ret.pop('passwd')
    result['user']=ret

@user_api.route('/private/user/get_attention_projects',methods=['GET'])
@require_token
@json_response
def get_attention_projects(result,user):

    projects=Project.query.outerjoin(Attention).outerjoin(User).filter(Attention.user_id==user.id).all()

    result['projects']=result_set_convert.models_2_arr(projects)

@user_api.route('/private/user/attention_project',methods=['POST'])
@require_token
@json_response
def attention_project(result,user):
    data=request.get_json()
    attention=Attention(user_id=user.id,project_id=data['project_id'])
    db.session.add(attention)
    db.session.commit()

@user_api.route('/private/user/apply_artist',methods=['POST'])
@require_token
@json_response
def apply_artist(result,user):

    data=request.get_json()
    artist=ArtistProfile()  
    artist.user_id=user.id
    artist.blood=data.get('blood','')
    artist.weight=data.get('weight',0)
    artist.height=data.get('height',0)
    artist.real_name=data['real_name']
    artist.nick_name=data['nick_name']
    artist.sina=data.get('sina','')
    artist.description=data.get('description',"")
    artist.popularity=0
    db.session.add(artist)
    db.session.commit()













