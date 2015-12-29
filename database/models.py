# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import inspect
from utils.result_set_convert import models_2_arr
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
        for field in [x for x in dir(self) if
                      not x.startswith('_') and x != 'metadata' and x != 'query' and x != 'query_class']:
            data = self.__getattribute__(field)
            if inspect.ismethod(data):
                continue
            elif isinstance(data, datetime.datetime):
                fields[field] = str(data)
            elif isinstance(data, BaseModel):
                fields[field] = data.as_map()
            else:
                fields[field] = data
        return fields

    def as_map(self):

        fields = {}
        for (key, value) in self.__dict__.items():
            if key.startswith('_'):
                continue
            elif isinstance(value, datetime.datetime):
                fields[key] = str(value)
            else:
                fields[key] = value
        return fields


class Admin(BaseModel):
    __tablename__ = 'admin'
    TYPE_SUPER = 1
    TYPE_NORMAL = 2
    account = db.Column('account', db.String(64))
    passwd = db.Column('passwd', db.String(32))
    admin_type = db.Column('admin_type', db.Integer)


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
    __tablename__ = "art_category"
    name = db.Column('name', db.String(32))
    display_order = db.Column('display_order', db.Integer)

    def __unicode__(self):
        return self.name


class ArtistProfile(BaseModel):
    __tablename__ = 'artist_profile'
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False)
    art_category_id = db.Column('art_category_id', db.Integer, db.ForeignKey('art_category.id'))
    art_category = db.relationship('ArtCategory', backref=db.backref('artist_profiles', lazy='dynamic'))
    # 0未审核 1审核
    is_checked = db.Column('is_checked', db.Integer, default=0)
    real_name = db.Column('real_name', db.String(64))
    nick_name = db.Column('nick_name', db.String(64))
    blood = db.Column('blood', db.String(16))
    photo = db.Column('photo', db.String(128))
    sina = db.Column('sina', db.String(128))
    description = db.Column('description', db.Text)
    height = db.Column('height', db.Integer)
    weight = db.Column('weight', db.Integer)
    popularity = db.Column('popularity', db.Integer)
    photos = db.relationship('ArtistPhoto', backref=db.backref('artist_profile', lazy='select'), lazy='select')

    def as_map(self):
        fields = super(ArtistProfile, self).as_map()
        fields['photos'] = models_2_arr(self.photos)
        return fields


class ArtistPhoto(BaseModel):
    __tablename__ = 'artist_photo'
    path = db.Column('path', db.String(512))
    display_order = db.Column('display_order', db.Integer)
    artist_profile_id = db.Column('artist_profile_id', db.Integer, db.ForeignKey('artist_profile.id'))


class Token(BaseModel):
    __tablename__ = 'token'
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('token', lazy='dynamic'))
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
    total_money = db.Column('total_money', db.DECIMAL(10, 2))
    current_money = db.Column('current_money', db.DECIMAL(10, 2))
    support_times = db.Column('support_times', db.Integer)

    category_id = db.Column('category_id', db.Integer, db.ForeignKey('catgory.id'))
    category = db.relationship('Category', backref=db.backref('projects', lazy='dynamic'))
    # status 1：进行中 2：已完成 3：失败 4：删除
    status = db.Column('status', db.Integer, default=1)
    # 1表示推荐 0表示未推荐
    is_recommend = db.Column('is_recommend', db.Integer, default=0)
    status = db.Column('status', db.Integer, default=1)  # 1为支付，2支付成功，3发货，4完成
    cover_image = db.Column('cover_image', db.String(512))

    publisher_id = db.Column('publisher_id', db.Integer, db.ForeignKey('user.id'))

    publisher = db.relationship('User', backref=db.backref('projects', lazy='dynamic'))

    def get_complete_rate(self):
        return int(self.current_money / self.total_money * 100)

    def as_map(self):
        fields = super(Project, self).as_map()
        fields['category'] = self.category.as_map()
        if fields['cover_image']:
            (name, ext) = os.path.splitext(fields['cover_image'])
            fields['cover_image_thumbnail'] = name + '_thumbnail' + ext
        else:
            fields['cover_image_thumbnail'] = None
        return fields

    def __unicode__(self):
        return self.title


class Payback(BaseModel):
    __tablename__ = 'payback'
    project_id = db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
    project = db.relationship('Project', backref=db.backref('paybacks', lazy='dynamic'))
    money = db.Column('money', db.DECIMAL(10, 2))
    title = db.Column('title', db.String(32))
    detail = db.Column('detail', db.String(512))
    payback_after_days = db.Column('payback_after_days', db.Integer)
    # 1无需物流 2 全国包邮（含港澳台）3 全国包邮不含港澳台
    delivery_mode = db.Column('delivery_mode', db.Integer, default=1)
    # 0 表示不限制 大于0表示具体的限制数量
    limit = db.Column('limit', db.Integer, default=0)

    delivery_money = db.Column('delivery_money', db.DECIMAL(10, 2), default=0)
    cover_image = db.Column('cover_image', db.String(512))
    total = db.Column('total', db.Integer)
    sold = db.Column('sold', db.Integer)

    def __unicode__(self):
        return self.title

    def as_map(self):
        fields = super(Payback, self).as_map()
        if fields['cover_image']:
            (name, ext) = os.path.splitext(fields['cover_image'])
            fields['cover_image_thumbnail'] = name + '_thumbnail' + ext
        else:
            fields['cover_image_thumbnail'] = None
        return fields


class Order(BaseModel):
    __tablename__ = 'order'

    STATUS_SUBMIT = 1
    STATUS_CANCEL = 2
    STATUS_PAY = 4
    STATUS_SEND = 8
    STATUS_SUCESS = 16
    STATUS_REBACK = 32

    order_no = db.Column('order_no', db.String(16))
    address_id = db.Column('address_id', db.ForeignKey("address.id"))
    address = db.relationship('Address', backref=db.backref('orders', lazy='dynamic'))

    # 购买着id
    buyer_id = db.Column('buyer_id', db.Integer, db.ForeignKey('user.id'))
    publisher_id = db.Column('publisher_id', db.Integer, db.ForeignKey('user.id'))

    buyer = db.relationship('User', foreign_keys=[buyer_id])
    publisher = db.relationship('User', foreign_keys=[publisher_id])

    payback_id = db.Column('payback_id', db.Integer, db.ForeignKey('payback.id'))
    payback = db.relationship('Payback', backref=db.backref('orders', lazy='dynamic'))

    project_id = db.Column('project_id', db.Integer, db.ForeignKey('project.id'))

    project = db.relationship('Project', backref=db.backref('orders', lazy='dynamic'))

    delivery_money = db.Column('delivery_money', db.DECIMAL(10, 2))
    total_money = db.Column('total_money', db.DECIMAL(10, 2))
    status = db.Column('status', db.Integer)

    payback_money = db.Column('payback_money', db.DECIMAL(10, 2))
    amount = db.Column('amount', db.Integer)


class Attention(BaseModel):
    __tablename__ = 'attention'
    project_id = db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))


class Address(BaseModel):
    __tablename__ = 'address'
    recieve_man = db.Column('recieve_name', db.String(32))
    phone = db.Column('phone', db.String(11))
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    address = db.Column('address', db.String(512))
    # 0 1默认地址
    default = db.Column('default', db.Integer, default=0)

    def __unicode__(self):
        return self.address



class UserSupportProject(BaseModel):
    __tablename__ = 'user_support_project'
    user_id = db.Column('user_id', db.Integer)
    project_id = db.Column('project_id', db.Integer)
    payback_id = db.Column('payback_id', db.Integer)


class ProjectPost(BaseModel):
    '''用于电影众酬推荐的海报设置，分为两种类型
        1. 点击之后跳转到一个url连接，外部浏览器打开
        2. 推荐的是一个众酬项目，点击之后跳转到相应的project详情界面
        3. 当post_type=1的时候，link必须设置
        4. 当post_type=2的时候，project_id必须设置
    '''
    __tablename__ = 'project_post'
    POST_LINK = 1
    POST_PROJECT = 2
    description = db.Column('description', db.String(512))
    image_url = db.Column('image_url', db.String(128))
    post_type = db.Column('post_type', db.Integer)
    project_id = db.Column('project_id', db.Integer)
    link = db.Column('link', db.String(128))


class ArtistPost(BaseModel):
    __tablename__ = 'artist_post'
    POST_LINK = 1
    POST_ARTIST = 2
    description = db.Column('description', db.String(512))
    image_url = db.Column('image_url', db.String(128))
    post_type = db.Column('post_type', db.Integer)
    artist_profile_id = db.Column('project_id', db.Integer)
    link = db.Column('link', db.String(128))


class ActivityNotice(BaseModel):
    __tablename__ = 'activity_notice'
    title = db.Column('title', db.String(256))
    content = db.Column('content', db.String(512))
    image_url = db.Column('image_url', db.String(128))
