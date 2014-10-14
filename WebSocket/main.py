#encoding: utf-8
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os
import Allhandlers
import urls


class Application(tornado.web.Application):
    def __init__(self):
        self.shoppingCart = Allhandlers.ShoppingCart()
        handlers = urls.handlers
        settings = {
            'template_path': os.path.join(os.path.dirname(__file__),'templates'),
            'static_path': os.path.join(os.path.dirname(__file__),'static')
        }

        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()