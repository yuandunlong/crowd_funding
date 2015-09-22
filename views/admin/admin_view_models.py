#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-09-21 22:50:38
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-09-22 17:17:58
from flask_admin.contrib.sqla import ModelView

from database.models import Token,Project,db,User,Category,Payback
from flask.ext.admin.form.upload import ImageUploadField
from wtforms import fields, widgets

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
    def __init__(self, session):
        super(TokenModelView,self).__init__(Token, db.session,name=u'令牌')

class CategoryModelView(ModelView):
    details_modal=True
    page_size=10
    column_list=('id','name','updated_time','created_time')
    column_labels=dict(id=u'序号',name=u'名称',updated_time=u'更新时间',created_time=u'创建时间')
    def __init__(self, session):
        super(CategoryModelView,self).__init__(Category, db.session,name=u'分类')

class UserModelView(ModelView):
    inline_models=(Token,)
    page_size=10
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
    form_overrides = dict(description=CKTextAreaField,cover_image=ImageUploadField)    
    page_size=10
    inline_models=(Payback,)
    column_list=('id','title','total_money','current_money','support_times','status','deadline_time','status')
    form_create_rules = ('category','title', 'total_money', 'current_money','status','cover_image','deadline_time','support_times','description','paybacks')

    column_labels=dict(category=u'分类',id=u'序号',title=u'标题',total_money=u'总金额',current_money=u'当前金额',status=u"状态",deadline_time=u'截至日期',support_times=u'支持数',updated_time=u'更新时间',created_time=u'创建时间',description=u'详情')
    column_searchable_list=('title',Project.title)
    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'
    def __init__(self, session):
        super(ProjectModelView, self).__init__(Project, db.session,name=u'项目')


class PaybackModelView(ModelView):
    def __init__(self, session):
        super(PaybackModelView,self).__init__(Payback, db.session,name=u'回报')


    