#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-09-21 22:50:38
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-11-07 14:11:16
from flask_admin.contrib.sqla import ModelView

from database.models import Token,Project,db,User,Category,Payback,ArtistProfile,ArtCategory,ArtistPhoto,ActivityNotice,ProjectPost,ArtistPost,Order
from flask.ext.admin.form.upload import ImageUploadField
from wtforms import fields, widgets
from flask_admin import form
import os.path as op
from werkzeug import secure_filename
from datetime import datetime
from jinja2 import Markup
def prefix_name(obj, file_data):
    parts = op.splitext(file_data.filename)
    return secure_filename('%s%s' % parts)


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
    column_searchable_list = ('mobile', User.mobile)
    column_filters = ('name', 'mobile', 'status')
    column_descriptions=dict(sex=u'1为男 2为女，其他数字代表未设置')
    form_choices={
        "sex":[('1','男'),('2','女')]
    }
    # 1 注册未激活 2激活 3 封号，4 删除
    def status_f(v,c,m,p):
        content=""
        if m.status==1:
            content=u'未激活'
        if m.status==2:
            content=u'激活'
        if m.status==3:
            content=u'封号'
        if m.status==4:
            content=u'删除'
        return content

    column_formatters=dict(status=status_f,sex=l)

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
    #form_columns=()
    can_view_details=True
    page_size=20
    inline_models=(Payback,)
    column_list=('id','title','total_money','current_money','support_times','deadline_time','status')
    form_create_rules = ('category','title', 'total_money', 'current_money','status','cover_image','deadline_time','support_times','description','paybacks')
    column_labels=dict(category=u'分类',id=u'序号',title=u'标题',total_money=u'总金额',current_money=u'当前金额',status=u"状态",deadline_time=u'截至日期',support_times=u'支持数',updated_time=u'更新时间',created_time=u'创建时间',description=u'详情',cover_image=u"封面")
    column_searchable_list=('title',Project.title)
    column_filters=("title","total_money","current_money","support_times","deadline_time","status")
        #1：进行中 2：已完成 3：失败 4：删除
    def status_f(v,c,m,p):
        if m.status==1:
            return Markup(u'<font color="blue">进行中 </font>')
        if m.status==2:
            return Markup(u'<font color="green">已完成 </font>')
        if m.status==3:
            return Markup(u'<font color="red">失败 </font>')
        return u'未知'
    column_formatters=dict(status=status_f)
    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'


    def __init__(self, session):
        super(ProjectModelView, self).__init__(Project, db.session,name=u'项目')


class PaybackModelView(ModelView):

    page_size=20
    can_view_details=True
    column_list=('id','project','title','payback_after_days','money','total','sold','created_time','updated_time')
    column_labels=dict(id=u'序号',project=u'项目',title=u'标题',money=u'价格',payback_after_days=u'截至日期后',created_time=u'创建时间',updated_time=u'更新时间',total=u'总份数',sold=u'卖出份数',detail=u'详情',delivery_mode=u'配送方式',status=
        u'状态',cover_image=u'封面',limit=u'每人限制份数')
    column_searchable_list = ('title', Payback.title)
    form_extra_fields = {
        'cover_image': form.ImageUploadField(u'封面',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True),namegen=prefix_name,url_relative_path="upload/")
    }
    def __init__(self, session):
        super(PaybackModelView,self).__init__(Payback, db.session,name=u'回报')



class ArtistProfileModelView(ModelView):
    page_size=20
    can_view_details=True
    inline_models=(ArtistPhoto,)
    form_extra_fields = {
        'photo': form.ImageUploadField(u'封面',base_path=file_path,namegen=prefix_name,url_relative_path="upload/")
    }    
    column_list=('id','user','art_category','nick_name','real_name','weight','height','popularity')
    form_overrides = dict(description=CKTextAreaField)  
    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'
    def __init__(self, session):
        super(ArtistProfileModelView,self).__init__(ArtistProfile, db.session,name=u'艺术家')


class ArtCategoryModelView(ModelView):
    page_size=20
    column_list=('id','name','display_order','created_time','updated_time')
    column_labels=dict(id=u'序号',name=u'名称',display_order=u'展示顺序',created_time=u'创建时间',updated_time=u'更新时间')
    def __init__(self):
        super(ArtCategoryModelView,self).__init__(ArtCategory,db.session,name=u"艺术家分类")

class ArtistPhotoModelView(ModelView):
    page_size=20

    form_extra_fields = {
        'path': form.ImageUploadField(u'封面',base_path=file_path,namegen=prefix_name,url_relative_path="upload/")
    }

    def __init__(self):
        super(ArtistPhotoModelView,self).__init__(ArtistPhoto,db.session,name=u'艺人照片')


class ActivityNoticeModelView(ModelView):
    page_size=20
    
    form_extra_fields = {
        'image_url': form.ImageUploadField(u'图片', base_path=file_path,namegen=prefix_name,url_relative_path="upload/post")
    }    
    
    def __init__(self):
        super(ActivityNoticeModelView,self).__init__(ActivityNotice,db.session,name=u'活动通知')


class ProjectPostModelView(ModelView):
    page_size=20


    form_extra_fields = {
        'image_url': form.ImageUploadField(u'图片', base_path=file_path,namegen=prefix_name,url_relative_path="upload/post")
    }

    def __init__(self):
        super(ProjectPostModelView,self).__init__(ProjectPost,db.session,name=u'电影海报')
   
    
class ArtistPostModelView(ModelView):
    page_size=20
    form_extra_fields = {
        'image_url': form.ImageUploadField(u'图片', base_path=file_path,namegen=prefix_name,url_relative_path="upload/post")
    }    
    
    def __init__(self):
        super(ArtistPostModelView,self).__init__(ArtistPost,db.session,name=u'艺人海报')

class OrderModelView(ModelView):
    page_size = 20
    column_list=('payback','buyer','order_no','status','created_time','updated_time')
    column_labels=dict(address=u"地址",buyer=u'购买者',project=u'项目',payback=u'回报')
    def payback_image_f(v,c,m,p):
        return Markup('<img style="width:80px;height:80px" src=/static/upload/'+m.payback.cover_image+'></img>')
    column_formatters=dict(payback=payback_image_f)
    def __init__(self):
        super(OrderModelView,self).__init__(Order,db.session,name=u'订单')