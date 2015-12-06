#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-11-07 13:05:33
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-11-07 13:21:40

from flask import Blueprint,request,current_app
from database.models import Order,Project,Payback,db
from utils.decorator import json_response,require_token
from utils.stringutil import build_order_no
from utils.result_set_convert import models_2_arr
order_api=Blueprint("order_api",__name__)

@order_api.route('/private/order/get_order_by_page',methods=['POST'])
@require_token
@json_response
def get_order_by_page(result,user):
    
    data=request.get_json()
    page=int(data.get('page',1))
    page_size=int(data.get('page_size',20))    
    
    status=data.get('status',None)
    
    payback_id=data.get('payback_id',None)
    
    project_id=data.get('project_id',None)
    
    
    query=Order.query
    if status:
        query=query.filter_by(status=status)
        
    if payback_id:
        query=query.filter_by(payback_id=payback_id)
        
    if project_id:
        query=query.filter_by(project_id=project_id)
    
    
    query=query.filter_by(user_id=user.id)    
    paginate=query.paginate(page,page_size)
    result['orders']=models_2_arr(paginate.items)


@order_api.route('/private/order/submit_order',methods=['POST'])
@require_token
@json_response
def submit_order(result,user):
    data=request.get_json()
    
    payback_id=int(data['payback_id'])
    payback=Payback.query.get(payback_id)
    project_id=int(data['project_id'])    
    amount=int(data['amount'])    
    project=Project.query.get(project_id)
    delivery_money=data.get('delivery_money',0)
    address_id=data['address_id']
    if project and payback:
        try:
            #自动开启事务
            order=Order()
            order.order_no=build_order_no()
            order.payback_id=payback_id
            order.buyer_id=int(user.id)
            order.delivery_money=delivery_money
            order.status=Order.STATUS_SUBMIT
            order.total_money=payback.money*amount+delivery_money
            order.payback_money=payback.money
            order.address_id=address_id
            order.amount=amount
            order.project_id=payback.project_id
            order.publisher_id=payback.project.publisher_id
            db.session.add(order)
            db.session.commit()
            print order.id
            order=Order.query.get(order.id)
            result['order']=order.as_map()

        except Exception as e:
            current_app.logger.exception(e)
            db.session.rollback()

        
        
        
   
    
    
    
    
    
