#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-09-18 10:04:17
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-09-23 21:05:35
# -*- coding: utf-8 -*-

from flask import Flask,url_for,Response,request,session
from database.models import db,User,Project,Token,Payback,Category
from views.user_ctrl import user_ctrl
from views.api.user_api import user_api
from views.api.category_api import category_api
from views.api.project_api import project_api
from views.admin.admin_ctrl import admin_ctrl
from views.admin.admin_project_ctrl import admin_project_ctrl
from views.admin.admin_user_ctrl import admin_user_ctrl
from logging.handlers import RotatingFileHandler
from logging import Formatter
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from views.admin.admin_view_models import UserModelView,ProjectModelView,CategoryModelView,TokenModelView,PaybackModelView
import logging
from flask.ext.babelex import Babel
from flask_admin.contrib.fileadmin import FileAdmin
from views.admin import admin_view_models
import os.path as op

log_roll_handler=RotatingFileHandler('roll.log',maxBytes=1024*1000*10)

log_roll_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
))

app = Flask(__name__)
db.init_app(app)
app.config.from_pyfile('app.cfg')
log_roll_handler.setLevel(logging.INFO)
app.logger.addHandler(log_roll_handler)
app.register_blueprint(user_ctrl)

app.register_blueprint(admin_ctrl,url_prefix='/admin2')
app.register_blueprint(admin_project_ctrl,url_prefix='/admin2')
app.register_blueprint(admin_user_ctrl,url_prefix='/admin2')

app.register_blueprint(user_api,url_prefix='/api')
app.register_blueprint(category_api,url_prefix='/api')
app.register_blueprint(project_api,url_prefix='/api')


babel = Babel(app)
@babel.localeselector
def get_locale():
    return 'zh_CN'
def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint)
            links.append((url, rule.endpoint))
    result=''
    for link in links:
        result=(result+link[0]+'&nbsp : &nbsp'+link[1]+'<br>')
    
    return Response(result)

path = op.join(op.dirname(__file__), 'static/upload')
admin_view_models.file_path=path

admin = Admin(app, name=u'乐事电影管理平台',template_mode='bootstrap3')
admin.add_view(UserModelView(db.session))
admin.add_view(CategoryModelView(db.session))
admin.add_view(ProjectModelView(db.session))
admin.add_view(PaybackModelView(db.session))
admin.add_view(TokenModelView(db.session))

admin.add_view(FileAdmin(path, '/static/upload/', name='上传文件管理'))
def create_app(config=None):
    app = Flask(__name__)
    db.init_app(app)
    app.config.from_pyfile('app.cfg')
    # configure your app...
    return app
if __name__ == '__main__':
    import sys
    reload(sys) 
    sys.setdefaultencoding( "utf-8" )   
    from os import environ
    ##db.create_all(bind='__all__', app=app)
    app.debug=True
    app.run(host='0.0.0.0',port=environ.get("PORT", 5000))
    #app.run('0.0.0.0:5050')
