#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-09-16 10:10:27
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-09-16 11:19:12
from flask import request,render_template,Blueprint
from services import user_service
admin_user_ctrl=Blueprint('admin_user_ctrl',__name__)
@admin_user_ctrl.route('/user/list',methods=['GET','POST'])
def user_list():
    (users,paginate)=user_service.query_users_by_page()
    return render_template('admin/user/user_list.html',users=users,paginate=paginate,title='会员管理')