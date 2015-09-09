from flask import request, Blueprint,json,Response,current_app
from utils.decorator import json_response,require_token
from database.models import Token,User,db
from services import user_service
from hashlib import md5
user_api=Blueprint("user_api",__name__ )

@user_api.route("/private/user/get_challenge",methods=['GET'])
@json_response
def get_challenge(result):
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
@user_api.route('/public/user/send_sms_code')
@json_response
def send_sms_code(result):
    pass


@user_api.route('/private/user/get_user_info',methods=['POST'])
@require_token
@json_response
def get_user_info(result,user):
    ret=user.as_map()
    ret.pop('passwd')
    result['user']=ret