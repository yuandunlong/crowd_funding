#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-09-10 17:56:29
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-09-10 19:58:29
from database.models import Admin
from hashlib import md5
from flask import g,session
def authentic(account,passwd):

    admin=Admin.query.filter_by(account=account).first()
    if not admin:
        return False
    else:
        m=md5()
        m.update(passwd)
        passwd=m.hexdigest()
        if passwd==admin.passwd:
            g.admin=admin
            session['admin_id']=admin.id
            return True
        else:
            return False



