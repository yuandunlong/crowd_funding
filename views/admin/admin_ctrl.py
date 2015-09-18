#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-09-18 10:04:17
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-09-18 10:04:31
# -*- coding: utf-8 -*-

from flask import request,Blueprint,render_template,redirect,url_for,session,current_app
from services import admin_service,category_service
admin_ctrl=Blueprint('admin_ctrl', __name__)

@admin_ctrl.before_request
def before_request():
    if request.path !='/admin/login' and request.path!='/admin/do_login' and session.get('admin_id',None) is None:
        return redirect('/admin/login')

@admin_ctrl.route('/index')
def admin_index():
    return render_template("admin/index.html")


@admin_ctrl.route('/login',methods=['GET'])
def admin_login():
    return render_template("admin/login.html")

@admin_ctrl.route('/do_login',methods=['POST'])
def do_admin_login():
    account=request.form.get('account','')
    passwd=request.form.get('password','')
    print url_for('.admin_index')
    if admin_service.authentic(account,passwd):
        return redirect(url_for('.admin_index'))
    else:
        return redirect(url_for('.admin_login'))

@admin_ctrl.route('/category/list',methods=['GET'])
def category_list():

    cats=category_service.get_all_categories()

    return render_template('admin/category/list.html',cats=cats,title=u'分类管理',menu_categories=True)




    


