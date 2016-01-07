#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-09-10 22:16:29
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-11-18 19:59:27
from flask import request, Blueprint,json,Response,current_app
from utils.decorator import json_response,require_token
from database.models import Token,User,db,Attention,Project,ArtistProfile,Address,Work,ArtistPhoto
from services import user_service
from hashlib import md5
from werkzeug.contrib.cache import SimpleCache
from utils.sms import sendTemplateSMS
from utils import stringutil,result_set_convert
from utils.result_set_convert import models_2_arr
user_api=Blueprint("user_api",__name__ )
sms_code_cache = SimpleCache(threshold=5000, default_timeout=300)
@user_api.route("/private/user/get_challenge",methods=['POST'])
@json_response
def get_challenge(result):
    data=request.get_json()
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

@user_api.route('/private/user/get_user_info',methods=['GET'])
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

@user_api.route('/private/user/del_attention_project',methods=['POST'])
@require_token
@json_response
def del_attention_project(result,user):
    data=request.json
    Attention.query.filter_by(user_id=user.id,project_id=data['project_id']).delete()
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
    artist.real_name=data.get('real_name','')
    artist.nick_name=data.get('nick_name','')
    artist.sina=data.get('sina','')
    artist.qq=data.get('qq','')
    artist.wexin=data.get('wexin','')
    artist.description=data.get('description',"")
    artist.popularity=0
    artist.life_experience=data.get('life_experience','')
    artist.photo=data.get('photo','')
    artist.art_category_id=data['art_category_id']
    db.session.add(artist)
    db.session.commit()

    works=data.get('works',None)
    if works:
        for work in works:
            work_model=Work(title=work.get('title',''),actor=work.get('actor',''),main_actor=work.get('main_actor'),director=work.get('director',''),image_url=work.get('image_url',''))
            work_model.artist_profile_id=artist.id
            db.session.add(work_model)
            db.session.commit()

    photos=data.get('photos',None)
    if photos:
        for photo in photos:
            artist_photo=ArtistPhoto()
            artist_photo.artist_profile_id=artist.id
            artist_photo.display_order=1
            artist_photo.path=photo['path']
            db.session.add(artist_photo)
            db.session.commit()




@user_api.route('/private/user/get_user_addresses',methods=['GET'])   
@require_token
@json_response
def get_user_addresses(result,user):
    addresses=Address.query.filter_by(user_id=user.id).all()
    arr=models_2_arr(addresses)
    result['addresses']=arr
    
@user_api.route('/private/user/get_user_default_address',methods=['GET'])   
@require_token
@json_response    
def get_user_default_address(result,user):
    address=Address.query.filter_by(user_id=user.id,default=1).first()
    if address:
        result['address']=address.as_map()
        
    
@user_api.route('/private/user/add_user_address',methods=['POST'])
@require_token
@json_response
def add_user_address(result,user):
    
    data=request.json
    phone=data['phone']
    recieve_man=data['recieve_man']
    address=data['address']
    
    add=Address()
    add.user_id=user.id
    add.recieve_man=recieve_man
    add.address=address
    add.phone=phone
    db.session.add(add)
    db.session.commit()

@user_api.route('/private/user/del_user_address',methods=['POST'])
@require_token
@json_response
def del_user_address(result,user):
    data=request.json
    address_id=data['address_id']
    Address.query.filter_by(id=address_id).delete()
    db.session.commit()



    
        













