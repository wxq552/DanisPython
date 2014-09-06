import tornado.httpserver
import tornado.ioloop
import tornado.web
import os
import urls
from tornado.options import define,options

define("port",default=8000,help="run on the given port",type=int)
class Application(tornado.web.Application):
    def __init__(self):
        handlers = urls.handler 
        settings = dict(template_path = os.path.join(os.path.dirname(__file__),"templates"),
                   static_path = os.path.join(os.path.dirname(__file__),"static"))
        tornado.web.Application.__init__(self, handlers, **settings)
        
if __name__ == "__main__":
    tornado.options.parse_command_line()
    application  = Application()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()