#encoding: utf-8
import tornado.web
import pymongo
class IndexHandler(tornado.web.RequestHandler):
    def get(self,page=1):
        self.pagesize = 3
        conn = pymongo.Connection("localhost",27017)
        db = conn.myblog
        articles = db.articles
        list = articles.find()[:6]
        count = articles.find().count()
        if count % self.pagesize == 0:
            pagecount = count/self.pagesize
        else:
            pagecount = count/self.pagesize + 1
        all = articles.find().sort("post_time",pymongo.DESCENDING).skip((int(page)-1)*self.pagesize).limit(self.pagesize)
        conn.close()
        self.render("index.html",articles=list,all_articles=all,pagecount=pagecount,page=page)
    