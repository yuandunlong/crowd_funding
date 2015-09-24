#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-09-21 22:50:38
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-09-24 11:19:19
from flask_admin.contrib.sqla import ModelView

from database.models import Token,Project,db,User,Category,Payback
from flask.ext.admin.form.upload import ImageUploadField
from wtforms import fields, widgets
from flask_admin import form
import os.path as op
from werkzeug import secure_filename
from datetime import datetime
def prefix_name(obj, file_data):
    parts = op.splitext(file_data.filename)
    return secure_filename('file-'+str(datetime.now())+'-%s%s' % parts)


file_path="static/upload"
class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(fields.TextAreaField):
    widget = CKTextAreaWidget() 

l=lambda x1,x2,x3,x :u'女' if x==1 else u'男'

class TokenModelView(ModelView):
    page_size=20
    column_list=('id','user','token','challenge','created_time','updated_time','expires')
    column_labels=dict(id=u'序号',user=u'用户手机号码',token=u'令牌',challenge=u'挑战码',updated_time=u'更新时间',created_time=u'创建时间',expires=u'过期时间')
    column_filters=("user.mobile","challenge","id")
    def __init__(self, session):
        super(TokenModelView,self).__init__(Token, db.session,name=u'令牌')

class CategoryModelView(ModelView):
    details_modal=True
    page_size=20
    column_list=('id','name','updated_time','created_time')
    column_labels=dict(id=u'序号',name=u'名称',updated_time=u'更新时间',created_time=u'创建时间')
    def __init__(self, session):
        super(CategoryModelView,self).__init__(Category, db.session,name=u'分类')

class UserModelView(ModelView):
    inline_models=(Token,)
    page_size=20
    edit_modal=True
    details_modal=True
    create_modal=True
    column_list = ('id', 'mobile', 'email','sex','status')
    column_labels = dict(name=u'姓名', mobile=u'手机号码',email=u'邮件',sex=u'性别',status=u'状态',updated_time=u'更新时间',created_time=u'创建时间',passwd=u'密码',token=u'token')
    column_formatters=dict(sex=l)
    column_searchable_list = ('mobile', User.mobile)
    column_filters = ('name', 'mobile', 'status')
    column_descriptions=dict(sex=u'1为男 2为女，其他数字代表未设置')

    def __init__(self, session):
        super(UserModelView,self).__init__(User, db.session,name=u'用户')

    #column_sortable_list=('name')

class ProjectModelView(ModelView):
    form_overrides = dict(description=CKTextAreaField)    
    form_extra_fields = {
        'cover_image': form.ImageUploadField(u'封面',
                                      base_path=file_path,
                                      thumbnail_size=(222, 150, True),url_relative_path="upload/")
    }

    page_size=20
    inline_models=(Payback,)
    column_list=('id','title','total_money','current_money','support_times','deadline_time','status')
    form_create_rules = ('category','title', 'total_money', 'current_money','status','cover_image','deadline_time','support_times','description','paybacks')
    column_labels=dict(category=u'分类',id=u'序号',title=u'标题',total_money=u'总金额',current_money=u'当前金额',status=u"状态",deadline_time=u'截至日期',support_times=u'支持数',updated_time=u'更新时间',created_time=u'创建时间',description=u'详情',cover_image=u"封面")
    column_searchable_list=('title',Project.title)
    column_filters=("title","total_money","current_money","support_times","deadline_time","status")
    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'
    def __init__(self, session):
        super(ProjectModelView, self).__init__(Project, db.session,name=u'项目')


class PaybackModelView(ModelView):

    page_size=20
    column_list=('id','project','title','payback_after_days','money','created_time','updated_time')
    column_labels=dict(id=u'序号',project=u'项目',title=u'标题',money=u'价格',payback_after_days=u'截至日期后',created_time=u'创建时间',updated_time=u'更新时间')
    column_searchable_list = ('title', Payback.title)
    form_extra_fields = {
        'cover_image': form.ImageUploadField(u'封面',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True),namegen=prefix_name,url_relative_path="upload/")
    }
    def __init__(self, session):
        super(PaybackModelView,self).__init__(Payback, db.session,name=u'回报')

   
    



    