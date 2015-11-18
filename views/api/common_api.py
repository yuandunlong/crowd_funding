#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-11-07 13:05:33
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-11-07 13:21:40
from flask import request,Blueprint
from utils.decorator import json_response
from utils.result_set_convert import models_2_arr
from database.models import ArtCategory,ProjectPost,ArtistPost,ActivityNotice
common_api=Blueprint(__name__,'common_api')
@common_api.route("/public/common/get_artist_category",methods=['GET'])
@json_response
def get_artist_category(result):
    artCategories=ArtCategory.query.all()
    arr=[]
    for item in artCategories:
        arr.append(item.as_map())
    result['art_categories']=arr
    
    
@common_api.route('/public/common/get_project_post',methods=['GET'])
@json_response
def get_project_post(result):
    
    pps=ProjectPost.query.all()
    result['project_posts']=models_2_arr(pps)
    
@common_api.route('/public/common/get_artist_post',methods=['GET'])
@json_response
def get_artist_post(result):
    aps=ArtistPost.query.all()
    result['artist_posts']=models_2_arr(aps)
    
@common_api.route('/public/common/get_activity_notice',methods=['GET'])
@json_response
def get_activity_notice(result):
    ans=ActivityNotice.query.all()
    result['activity_notices']=models_2_arr(ans)
    
    
    
    
    
    





