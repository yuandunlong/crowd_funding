from functools import wraps
from flask import current_app,Response,request,g,redirect,url_for,session
from database.models import User,Token
from utils.json_encode import DateTimeEncoder
import traceback
import simplejson as json
import string
def json_response(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            result={'code':0,'msg':'ok'}
            if kwargs.has_key('user'):
                func(result,kwargs['user'])
            else:
                func(result)
        except Exception, e:
            current_app.logger.exception(e)
            result['code']=1
            result['msg']=traceback.format_exc()
        return Response(json.dumps(result),content_type='application/json')
    return wrapper


def require_token(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        access_token=request.args.get('token','')
        access_token=string.strip(access_token)
        result={'code':0,'msg':'ok'}
        if access_token=='':
            result['code']=1
            result['msg']='please provide a valid token'
            return Response(json.dumps(result),content_type='application/json')
        else:
            token=Token.query.filter_by(token=access_token).first()
            if not token:
                result['code']=1
                result['msg']='please provide a valid token'
                return Response(json.dumps(result),content_type='application/json')
        user=User.query.get(token.user_id)
        return func(user=user)

    return wrapper



