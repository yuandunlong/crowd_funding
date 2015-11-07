#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-09-24 09:54:51
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-11-07 13:06:42
from flask import request,Blueprint
from utils.decorator import json_response
from database.models import Payback,db

payback_api=Blueprint(__name__,'payback_api')

@payback_api.route('/public/payback/get_paybacks_by_project_id',methods=['POST'])
@json_response
def get_paybacks_by_project_id(result):
    data=request.get_json()
    project_id=data['project_id']

    paybacks=Payback.query.filter_by(project_id=project_id).all()
    arr=[]
    for payback in paybacks:
        arr.append(payback.as_map())
    result['paybacks']=arr