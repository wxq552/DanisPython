#encoding: utf-8
import tornado.web
from uuid import uuid4
import json
import pymongo
import time
import tornado.websocket
class ShoppingCart(object):
    def __init__(self):
        self.getconn()
    def getconn(self):
        self.conn = pymongo.Connection("localhost",27017)
        self.db = self.conn.message_db
        self.coll = self.db.message_coll
    callbacks = []  #保存回调函数的列表
    #messagelist = []  #后台消息队列
    #客户端注册回调函数
    def register(self, callback):
        self.callbacks.append(callback)
    #客户端移除回调函数
    def unregister(self, callback):
        self.callbacks.remove(callback)
    #将消息添加到消息队列
    def moveItemToCart(self,message):
        if self.conn is None:
            self.getconn()
        self.coll.insert(message)
        self.conn.close()
        self.notifyCallbacks()  #循环执行每个客户端注册的回调函数，执行回调函数就会将消息推送到每个与服务器建立起长连接的客户端
        #print self.messagelist

    def removeItemFromCart(self, session):
        if session not in self.messagelist:
            return

        del(self.messagelist[session])
        self.notifyCallbacks()

    def notifyCallbacks(self):
        for c in self.callbacks:
            #print c
            self.callbackHelper(c)
        #self.callbacks = []

    def callbackHelper(self, callback):    
        callback(self.getMessages())
    #返回消息队列
    def getMessages(self):
        if self.conn is None:
            self.getconn()
        message_list = self.coll.find()
        new_message_list = []
        for doc in message_list:
            del doc['_id']
            new_message_list.append(doc)
        self.conn.close()
        return new_message_list
    
class PushHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("Push.html")
        
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        session = uuid4()
        #count = self.application.shoppingCart.getInventoryCount()
        messagelist = self.application.shoppingCart.getMessages()
        self.render("index.html", session=session,messages=messagelist)

class CartHandler(tornado.web.RequestHandler):
    def post(self):
        title = self.get_argument('title')
        content = self.get_argument('content')
        date = time.time()
        message = dict(title=title,content=content,date=date)
        #将消息添加到后台消息队列
        self.application.shoppingCart.moveItemToCart(message)
        
        
class StatusHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.application.shoppingCart.register(self.callback)

    def on_close(self):
        self.application.shoppingCart.unregister(self.callback)

    def on_message(self, message):
        pass

    def callback(self, messagelist):
        self.write_message(json.dumps(messagelist))