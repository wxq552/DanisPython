#encoding: utf-8
import pymongo,time
conn = pymongo.Connection("localhost",27017)
db = conn.myblog
articles = db.articles
for i in range(2):
    localtime = time.localtime(time.time())
    date = time.strftime('%Y-%M-%d',localtime)
    articles.insert({
      "title" : "你是的撒旦是的撒旦",
      "content" : "速度速度撒打算山东省杜拉拉速度速度撒打算是的撒快回来快回来看好了山东省大数据后离开后立刻回来看好了",
      "author" : "Danis",
      "post_time" : date,
      "imgurl" : "img/HighRes-290x130.jpg",
      "comments":[{
      "content" : "速度速度撒打算山东省杜拉拉速度速度撒打算是的撒快回来快回来看好了山东省大数据后离开后立刻回来看好了",
      "author" : "Danis",
      "post_time" : date,
      "comments":[]
     },]
     })
    time.sleep(3)
    