#encoding: utf-8
import InitClient,pymongo,sched, time

#任务调度时间间隔
INTERVAL = 10
client = InitClient.get_client()
conn = pymongo.Connection("localhost",27017)
db = conn.datalist
weibodata = db.weibodata
#创建任务调度器
s = sched.scheduler(time.time, time.sleep)
#名人微博ID列表
ids = "3952070245L,1304194202,1223762662,3261134763L,1230663070"
#根据id获取昵称
def get_screen_names():
    screen_names = []
    for id in ids:
        screen_names.append((client.users.show.get(uid = id).screen_name,id))
    return screen_names

#根据提供的id列表获取微博数据
def getDataList():
    #screen_names = get_screen_names()
    for id in ids:
        #print id
        data = client.statuses.user_timeline.get(uid = id)
        datalist = data.statuses
        for d in datalist:
            print d.user.id
        #weibodata.remove()
        #weibodata.insert(datalist,save=True)
        
    #datalist = r.statuses
    #weibodata.remove()
    #weibodata.insert(datalist,save=True)

def getMyDatalist(tip):
    #id这个key
    key = str(u'id').decode('utf-8')
    #存储旧数据的id列表
    old_ids = []
    #存储新微博的列表
    extr_wb = []
    #从MongoDB上获取的数据
    old_datalist = weibodata.find()
    for old in old_datalist:
        old_ids.append(old[key])
        
    #从微博上抓取新数据
    data = client.statuses.user_timeline.get(count=40)
    new_datalist = data.statuses
    for new in new_datalist:
        if new[key] not in old_ids:
            extr_wb.append(new)
    if extr_wb:
        weibodata.insert(extr_wb,save=True)
    print tip
    
    for new in new_datalist:
        print new.text
    print 
"""发微博"""  
def post_text_weibo():
    client = InitClient.get_client()
    if not client:
        print 'Get client Error!'
        return

    # 发微博
    while True:
        print '你是否要发表一条新微博?(y/n):',
        choice = raw_input()
        if choice in ['y','Y']:
            content = raw_input('请输入微博内容:')
            if content:
                client.statuses.update.post(status = content)
                print '发表微博成功!'
                break;
            else:
                print '内容为空！发表失败！'
        if choice in ['n', 'N']:
            break
    #print client.statuses.update.post(status=u'测试OAuth 2.0发微博')
    #print "发表微博成功！"
#post_text_weibo()

"""发带图片的微博"""
def post_img_weibo():
    client = InitClient.get_client()
    print client.statuses.upload.post(status=u'测试OAuth 2.0带图片发微博', pic=open('resource/1.jpg'))
    print "发表带图片的微博"
#post_text_weibo()
#getDataList()
# screen_names = get_screen_names()
# for screen_name,id in screen_names:
#     print screen_name,id
           
#getDataList()

def jobtodo():
    #设置任务调度
    s.enter(INTERVAL, 1, getMyDatalist, ('刷新微博数据!!!',))
    #四个参数分别为：间隔事件、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数，给他
    #的参数（注意：一定要以tuple给如，如果只有一个参数就(xx,)）
    s.run()
    print time.ctime(time.time())
    


if __name__ == "__main__":
    getMyDatalist("hello world")
    #while True:
    #    jobtodo()
    #post_img_weibo()
    

