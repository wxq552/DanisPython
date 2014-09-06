import tornado.web
import os
import tornado.httpclient
import json
config = {}
execfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.py"), config) 

class AnwserHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.info = self.get_argument("info","")
        url = config['URL']+"?key="+config['KEY']+"&info="+self.info
        asyncclient = tornado.httpclient.AsyncHTTPClient()
        asyncclient.fetch(url,callback=self.on_response)
    def on_response(self,response):
        reback = json.loads(response.body)
        if not self.info:
            self.render("index.html",section = reback['text'])
        else:
            print response.body
            self.write(response.body)
            self.finish()