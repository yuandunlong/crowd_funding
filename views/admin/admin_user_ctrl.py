#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-09-16 10:10:27
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-09-22 13:53:19
from flask import request,render_template,Blueprint,session,redirect,make_response,Response,json
from services import user_service
from database.models import User,db
admin_user_ctrl=Blueprint('admin_user_ctrl',__name__)

@admin_user_ctrl.before_request
def before_request():
    if request.path !='/admin/login' and request.path!='/admin/do_login' and session.get('admin_id',None) is None:
        return redirect('/admin2/login')

@admin_user_ctrl.route('/user/list',methods=['GET','POST'])
def user_list():
    (users,paginate)=user_service.query_users_by_page()
    return render_template('admins/user/user_list.html',users=users,paginate=paginate,title='会员管理',menu_user=True )



@admin_user_ctrl.route('/user/delete',methods=['POST'])
def user_delete():
    result={'code':0,'msg':'ok'}
    data=request.get_json()
    user_id=data.get('user_id',0)
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return Response(json.dumps(result),content_type='application/json')