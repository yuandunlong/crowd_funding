from flask import Flask
from database.models import db
from views.user_ctrl import user_ctrl
from views.api.user_api import user_api
from views.api.category_api import category_api
from views.api.project_api import project_api
from views.admin.admin_ctrl import admin_ctrl
from logging.handlers import RotatingFileHandler
from logging import Formatter
import logging
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

app.register_blueprint(admin_ctrl,url_prefix='/admin')

app.register_blueprint(user_api,url_prefix='/api')
app.register_blueprint(category_api,url_prefix='/api')
app.register_blueprint(project_api,url_prefix='/api')
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
