from flask import Flask
from database.models import db
from views.user_ctrl import user_ctrl
from views.api.user_api import user_api
app = Flask(__name__)
db.init_app(app)
app.config.from_pyfile('app.cfg')
app.register_blueprint(user_ctrl)
app.register_blueprint(user_api,url_prefix='/api')

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
