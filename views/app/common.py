# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from utils.decorator import json_response

common_ctrl = Blueprint('common_ctrl', __name__)

#通过province返回city
@common_ctrl.route('/city', methods=['GET'])
@json_response
def get_city_by_province(result):
    #todo 接口实现
    data = [
        {1: '成都'},
        {2: '绵阳'}
    ]
    result['cities'] = data