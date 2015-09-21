# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

projects_ctrl = Blueprint('projects_ctrl', __name__)

@projects_ctrl.route('/list')
def projects_list():
    data = {
        'title': u"项目列表",
        'active': 'projects'
    }
    return render_template("app/projects/list.html",data = data)
