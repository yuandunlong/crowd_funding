#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-09-11 16:38:41
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-09-18 10:01:35

from flask import request,Blueprint
from utils.decorator import json_response
from services import category_service
category_api=Blueprint('category_api',__name__)

@category_api.route('/public/category/get_all_categories',methods=['GET'])
@json_response
def get_all_categories(result):
    cats=category_service.get_all_categories()
    cats_arr=[]
    for cat in cats:
        cats_arr.append(cat.as_map())
    result['categories']=cats_arr





