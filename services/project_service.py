# -*- coding: utf-8 -*-

from database.models import Project
def query_projects_by_page(titlelike=None,page=1,page_size=20,order_by='updated_time desc',querys=None):
    page=int(page)
    page_size=int(page_size)
    query=Project.query
    if querys:
        if querys.has_key('status') and querys['status'] != None:
            query=query.filter_by(status=querys['status'])
            print "++++++"
        if querys.has_key('is_recommend') and querys['is_recommend'] !=None:
            query=query.filter_by(is_recommend=querys['is_recommend'])
            print "------"
    if titlelike:
        paginate=query.filter(Project.title.like(u"%{}%".format(titlelike))).order_by(order_by).paginate(page,page_size)
    else:
        paginate=query.order_by(order_by).paginate(page,page_size)
    return paginate.items,paginate







