from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask_web import app
import sys
reload(sys) 
sys.setdefaultencoding( "utf-8" )   
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)
IOLoop.instance().start()