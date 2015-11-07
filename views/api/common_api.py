#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-11-07 13:05:33
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-11-07 13:21:40
from flask import request,Blueprint
from utils.decorator import json_response
from database.models import ArtCategory
common_api=Blueprint(__name__,'common_api')
@common_api.route("/public/common/get_artist_category",methods=['GET'])
@json_response
def get_artist_category(result):
    artCategories=ArtCategory.query.all()
    arr=[]
    for item in artCategories:
        arr.append(item.as_map())
    result['art_categories']=arr





