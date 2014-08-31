#encoding: utf-8
import pymongo
conn = pymongo.Connection("localhost")
db = conn.myweibo
access = db.access
access.insert({"nickname":"让大地哎呀的TUI秋","id_pic":"http://tp1.sinaimg.cn/2191865900/180/40055654291/1","access_token":"2.00o8q15CdK_9kDccc43326c41B3rUC"})

