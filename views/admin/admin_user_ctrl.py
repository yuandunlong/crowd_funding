#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-09-16 10:10:27
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-09-17 23:31:37
from flask import request,render_template,Blueprint,session,redirect
from services import user_service
admin_user_ctrl=Blueprint('admin_user_ctrl',__name__)

@admin_user_ctrl.before_request
def before_request():
    if request.path !='/admin/login' and request.path!='/admin/do_login' and session.get('admin_id',None) is None:
        return redirect('/admin/login')

@admin_user_ctrl.route('/user/list',methods=['GET','POST'])
def user_list():
    (users,paginate)=user_service.query_users_by_page()
    return render_template('admin/user/user_list.html',users=users,paginate=paginate,title='会员管理',menu_user=True )