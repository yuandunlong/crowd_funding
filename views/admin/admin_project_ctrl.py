#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-09-16 09:01:25
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-09-22 13:53:08

from flask import request,render_template,Blueprint,session,redirect
from services import project_service
admin_project_ctrl=Blueprint('admin_project_ctrl',__name__)

@admin_project_ctrl.before_request
def before_request():
    if request.path !='/admin2/login' and request.path!='/admin2/do_login' and session.get('admin_id',None) is None:
        return redirect('/admin2/login')


@admin_project_ctrl.route('/project/list',methods=['GET','POST'])
def project_list():
    page=request.args.get('page',1)
    page_size=request.args.get('page_size',20)
    title=None
    if request.method=='POST':
        title=request.forms.get('title',None)
    (projects,paginate)=project_service.query_projects_by_page(title)
    return render_template('admins/project/project_list.html',projects=projects,paginate=paginate,title=u'项目管理',menu_project=True)


