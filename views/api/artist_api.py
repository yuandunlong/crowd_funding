#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-11-07 13:05:33
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-11-07 13:21:40

from flask import Blueprint,request
from database.models import ArtistProfile,User
from utils.decorator import json_response
from utils.result_set_convert import models_2_arr
artist_api=Blueprint("artist_api",__name__)
@artist_api.route('/public/artist/get_artist_by_page',methods=['POST'])
@json_response
def get_artist_by_page(result):
    data=request.get_json()
    page=int(data.get('page',1))
    page_size=int(data.get('page_size',20))    
    
    cat_id=data.get('cat_id',None)
    if cat_id:
        paginate=ArtistProfile.query.filter_by(art_category_id=cat_id).paginate(page,page_size)
        
    else:
        paginate=ArtistProfile.query.paginate(page,page_size)
    result['artist']=models_2_arr(paginate.items)
    
    

