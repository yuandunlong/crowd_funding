# -*- coding: utf-8 -*-
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import inspect
import datetime
db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column('id', db.Integer, primary_key=True)
    created_time = db.Column(
        'created_time', db.TIMESTAMP, server_default=func.now())
    updated_time = db.Column(
        'updated_time', db.TIMESTAMP, server_default=func.now())

    def as_map(self):
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


class Token(BaseModel):
    __tablename__ = 'token'
    user_id = db.Column('user_id', db.Integer)
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
    category_id = db.Column('category_id', db.Integer)
    # status 1：进行中 2：已完成 3：失败 4：删除
    status = db.Column('status', db.Integer, default=1)


class Payback(BaseModel):
    __tablename__ = 'payback'
    project_id = db.Column('project_id', db.Integer)
    money = db.Column('money', db.DECIMAL)
    title = db.Column('title', db.String(32))
    detail = db.Column('detail', db.String(128))
    payback_after_days = db.Column('payback_after_days', db.Integer)
    image_url = db.Column('image_url', db.String(128))
    # 1无需物流 2 全国包邮（含港澳台）3 全国包邮不含港澳台
    delivery_mode = db.Column('delivery_mode', db.Integer, default=1)
    # 0 表示不限制 大于0表示具体的限制数量
    limit = db.Column('limit', db.Integer, default=0)
    status = db.Column('status', db.Integer, default=1)  # 1为支付，2支付成功，3发货，4完成


class Attention(BaseModel):
    __tablename__ = 'attention'
    id = db.Column('id', db.Integer, primary_key=True)
    project_id = db.Column('project_id', db.Integer)
    user_id = db.Column('user_id', db.Integer)


class UserSupportProject(BaseModel):
    __tablename__ = 'user_support_project'
    project_id = db.Column('project_id', db.Integer)
    payback_id = db.Column('payback_id', db.Integer)


class Category(BaseModel):
    __tablename__ = 'catgory'
    name = db.Column('name', db.String(32))
