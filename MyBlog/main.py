#encoding: utf-8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import urls
import os

from tornado.options import define,options
define("port", default=8000, help="run on the given port", type=int)

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__),"templates")
STATIC_DIR = os.path.join(os.path.dirname(__file__),"static")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = urls.handlers
        settings = dict(template_path = TEMPLATE_DIR,static_path = STATIC_DIR,debug =True,)
        tornado.web.Application.__init__(self, handlers, **settings)
    
def main():
    tornado.options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    
if __name__ == "__main__":
    main()
    
    
