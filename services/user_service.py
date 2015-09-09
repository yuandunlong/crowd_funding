# -*- coding: utf-8 -*-
import random
import string
from database.models import db, User


def get_challenge():
    access_token = map(lambda i: chr(random.randint(65, 90)), range(32))
    access_token=string.join(access_token,'')
    return access_token


def get_access_token():
    access_token = map(lambda i: chr(random.randint(65, 90)), range(32))
    access_token=string.join(access_token,'')
    return access_token


def get_user_by_id(user_id):
    user = User.query.get(user_id)
    return user


