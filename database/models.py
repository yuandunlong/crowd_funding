# -*- coding: utf-8 -*-
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import inspect
import datetime
import os
db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column('id', db.Integer, primary_key=True)
    created_time = db.Column(
        'created_time', db.TIMESTAMP, server_default=func.now())
    updated_time = db.Column(
        'updated_time', db.TIMESTAMP, server_default=func.now())

    def as_map2(self):
        fields = {}
        for field in [x for x in dir(self) if not x.startswith('_') and x != 'metadata' and x != 'query' and x != 'query_class']:
            data = self.__getattribute__(field)
            if inspect.ismethod(data):
                continue
            elif isinstance(data, datetime.datetime):
                fields[field]=str(data)
            else:
                fields[field] = data
        print fields
        return fields
    def as_map(self):

        fields={}
        for (key,value) in self.__dict__.items():
            if key.startswith('_'):
                continue
            elif isinstance(value,datetime.datetime):
                fields[key]=str(value)
            else:
                fields[key]=value
        return fields


class Admin(BaseModel):
    __tablename__ = 'admin'
    TYPE_SUPER=1
    TYPE_NORMAL=2
    account = db.Column('account', db.String(64))
    passwd = db.Column('passwd', db.String(32))
    admin_type = db.Column('admin_type',db.Integer)




class User(BaseModel):
    __tablename__ = 'user'
    mobile = db.Column('mobile', db.String(11))
    passwd = db.Column('passwd', db.String(32))
    # 1 注册未激活 2激活 3 封号，4 删除
    status = db.Column('status', db.Integer, default=1)
    name = db.Column('name', db.String(64))
    email = db.Column('email', db.String(64))
    sex = db.Column('sex', db.Integer, default=0)  # 1 男性 2：女性
    def __unicode__(self):
        return self.mobile
   # access_token=db.relationship('token',backref=db.backref('token', lazy='dynamic'))



class Category(BaseModel):
    __tablename__ = 'catgory'
    name = db.Column('name', db.String(32))
    def __unicode__(self):
        return self.name

class ArtCategory(BaseModel):
    __tablename__="art_category"
    name=db.Column('name',db.String(32))
    def __unicode__(self):
        return self.name

class ArtistProfile(BaseModel):
    __tablename__='artist_profile'
    user_id=db.Column('user_id',db.Integer,db.ForeignKey('user.id'))
    user=db.relationship('User',uselist=False)
    art_category_id=db.Column('art_category_id',db.Integer,db.ForeignKey('art_category.id'))
    art_category=db.relationship('ArtCategory',backref=db.backref('artists',lazy='dynamic'))
    #0未审核 1审核
    is_checked=db.Column('is_checked',db.Integer,default=0)
    real_name=db.Column('real_name',db.String(64))
    nick_name=db.Column('nick_name',db.String(64))
    blood=db.Column('blood',db.String(16))
    photo=db.Column('photo',db.String(128))
    sina=db.Column('sina',db.String(128))
    description=db.Column('description',db.Text)
    height=db.Column('height',db.Integer)
    weight=db.Column('weight',db.Integer)
    popularity=db.Column('popularity',db.Integer)


class Token(BaseModel):
    __tablename__ = 'token'
    user_id = db.Column('user_id', db.Integer,db.ForeignKey('user.id'))
    user=db.relationship('User',backref=db.backref('token',lazy='dynamic'))
    token = db.Column('token', db.String(32), unique=True)
    challenge = db.Column('challenge', db.String(16))  # 16位 挑战码
    # 验证码失效时间
    expires = db.Column('expires', db.Integer)


class Project(BaseModel):
    __tablename__ = 'project'
    title = db.Column('title', db.String(128))
    summary = db.Column('summary', db.Text)
    description = db.Column('description', db.Text)
    deadline_time = db.Column('deadline_time', db.DateTime)
    total_money = db.Column('total_money', db.DECIMAL)
    current_money = db.Column('current_money', db.DECIMAL)
    support_times = db.Column('support_times', db.Integer)

    category_id = db.Column('category_id', db.Integer,db.ForeignKey('catgory.id'))
    category=db.relationship('Category',backref=db.backref('projects',lazy='dynamic'))
    # status 1：进行中 2：已完成 3：失败 4：删除
    status = db.Column('status', db.Integer, default=1)
    # 1表示推荐 0表示未推荐
    is_recommend = db.Column('is_recommend',db.Integer,default=0)
    status = db.Column('status', db.Integer, default=1)  # 1为支付，2支付成功，3发货，4完成
    cover_image=db.Column('cover_image',db.String(512))

    def get_complete_rate(self):
        return int(self.current_money/self.total_money*100)
    def as_map(self):
        fields=super(Project,self).as_map()
        fields['category']=self.category.as_map()
        if fields['cover_image']:
            (name,ext)=os.path.splitext(fields['cover_image'])
            fields['cover_image_thumbnail']=name+'_thumbnail'+ext
        else:
            fields['cover_image_thumbnail']=None
        return fields

    def __unicode__(self):
        return self.title


class Payback(BaseModel):
    __tablename__ = 'payback'
    project_id = db.Column('project_id', db.Integer,db.ForeignKey('project.id'))
    project=db.relationship('Project',backref=db.backref('paybacks',lazy='dynamic'))
    money = db.Column('money', db.DECIMAL)
    title = db.Column('title', db.String(32))
    detail = db.Column('detail', db.String(512))
    payback_after_days = db.Column('payback_after_days', db.Integer)
    # 1无需物流 2 全国包邮（含港澳台）3 全国包邮不含港澳台
    delivery_mode = db.Column('delivery_mode', db.Integer, default=1)
    # 0 表示不限制 大于0表示具体的限制数量
    limit = db.Column('limit', db.Integer, default=0)
    status = db.Column('status', db.Integer, default=1)  # 1为支付，2支付成功，3发货，4完成
    cover_image=db.Column('cover_image',db.String(512))
    total=db.Column('total',db.Integer)
    sold=db.Column('sold',db.Integer)
    def as_map(self):
        fields=super(Payback,self).as_map()
        if fields['cover_image']:
            (name,ext)=os.path.splitext(fields['cover_image'])
            fields['cover_image_thumbnail']=name+'_thumbnail'+ext
        else:
            fields['cover_image_thumbnail']=None
        return fields

class Attention(BaseModel):
    __tablename__ = 'attention'
    project_id = db.Column('project_id', db.Integer,db.ForeignKey('project.id'))
    user_id = db.Column('user_id', db.Integer,db.ForeignKey('user.id'))




class Address(BaseModel):
    __tablename__='address'
    province_id=db.Column('province_id',db.Integer)
    city_id=db.Column('city_id',db.Integer)



class UserSupportProject(BaseModel):
    __tablename__ = 'user_support_project'
    project_id = db.Column('project_id', db.Integer)
    payback_id = db.Column('payback_id', db.Integer)

class ProjectPost(BaseModel):
    __tablename__='project_post'
    

