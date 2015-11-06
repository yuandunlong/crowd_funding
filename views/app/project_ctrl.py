# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
from services import project_service
project_ctrl = Blueprint('project_ctrl', __name__)

@project_ctrl.route('/list',methods=['GET'])
def projects_list():
    page=request.args.get('page',1)
    page_size=request.args.get('page_size',20)
    (items,paginate)=project_service.query_projects_by_page(page=page,page_size=page_size)

    data = {
        'title': u"项目列表",
        'active': 'projects',
        'projects':items,
        'paginate':paginate
    }


    return render_template("app/project/list.html",data = data)

@project_ctrl.route('/', methods=['GET'])
def publish_project():
    data = {
        'title': u"发布项目",
        'active': 'publish'
    }
    return render_template("app/project/publish.html", data = data)

@project_ctrl.route('/payback', methods=['POST'])
def createPayBack():
    #todo
    print request.form
    data=request.form
    return render_template("app/project/payback.html", data = data)


@project_ctrl.route('/project/upload_cover',methods='POST')
def upload_cover():
    pass

