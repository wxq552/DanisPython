#encoding: utf-8
from CNMThreadsGenerator import MyThread
from time import sleep
from Queue import Queue
import time
import logging
import os

logging.basicConfig(filename=os.path.join(os.getcwd(),"logs/log.txt"),filemode="w",
                    level=logging.DEBUG,format = '%(asctime)s - %(levelname)s: %(message)s')
log = logging.getLogger("root.log2")
delay = 0

ALARM_LEVEL1 = 1 #"黄图嫌疑，敏感词嫌疑"
ALARM_LEVEL2 = 2 #"黄图嫌疑"
ALARM_LEVEL3 = 3 #"敏感词嫌疑"
#实现每间隔1分钟扫描评论表获取最近一分钟发表的评论列表，并加到队列中
def writeQ(queue,dbpool):  
    global delay
    begin_time = time.time()-delay-60
    now = time.time()-delay
    local_begin_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(begin_time))
    local_now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(now))
    log.debug("开始扫描微博列表,并加入最近一分钟新发表的微博到队列中")
    log.debug("一分钟之前时间：%s",*(local_begin_time,))
    log.debug("当前时间：%s",*(local_now,))
    conn = dbpool.connection()
    cursor = conn.cursor()
    #cursor.execute("select comment_id,uid,reply_comment_id,reply_uid,weibo_id,content,ctime,isdel,ip from ts_weibo_comment where ctime>=%s and ctime<=%s",[begin_time,now])#order by comment_id desc limit 0,5")
    cursor.execute("select comment_id,uid,reply_comment_id,reply_uid,weibo_id,content,ctime,isdel,ip from ts_weibo_comment order by comment_id desc limit 0,5") 
    cm_list = cursor.fetchall()
    cursor.close()
    conn.close()
    delay = len(cm_list)
    for wb in cm_list:
        if int(wb[7]) == 0:
            queue.put(wb,1) 
    delay = time.time()-now #执行语句延迟了的时间，补回来，回到原来的时间点
#实现从队列中读取每一条评论，识别评论的图片及敏感词，若有问题，则将记录加入到队列中
def readQ(queue,queue1,testutil):  
    val=queue.get(1)  
    log.debug('从队列中取出一条评论出来检测')#队列长度为：',queue.qsize()
    if testutil.ContainBanWord(val[5]):
        record = [val[0],val[1],val[2],val[3],val[4],val[6],ALARM_LEVEL3,val[8]]
        queue1.put(record,1)
        log.debug("敏感词嫌疑！！！")
    else:
        log.debug("评论健康！！！")
#实现从队列中获取记录存储到数据库中
def addtoTable(queue1,dbpool):
    val = queue1.get(1)
    sql = "insert into ts_mb_iffy_comment (comment_id,uid,reply_comment_id,reply_uid,weibo_id,ctime,reason,ip) values (%s,%s,%s,%s,%s,%s,%s,%s)"
    conn = dbpool.connection()
    cursor = conn.cursor()
    cursor.execute(sql,val)
    conn.commit()
    cursor.close()
    conn.close()
    log.debug("已记录到的一条问题评论")
#负责间隔一定时间扫描数据表，拿到评论数据放到Queue中
def writer(queue,dbpool):
    while True:
        writeQ(queue,dbpool)
        sleep(60)

#负责从队列中取出评论进行过滤识别
def reader(queue,queue1,testutil):
    while True:  
        readQ(queue,queue1,testutil)  
        sleep(1)  
#负责从队列queue1中取出记录，保存到数据库        
def recorder(queue1,dbpool):
    while True:
        addtoTable(queue1,dbpool)
        sleep(1)
    
def Comment_main(dbpool,testutil):   
    q=Queue(0)
    q1 = Queue(0)  
    threads=[]  
      
    #扫描评论的线程
    t1 = MyThread(writer,(q,dbpool),writer.__name__)
    threads.append(t1)
    #识别过滤的线程
    t2 = MyThread(reader,(q,q1,testutil),reader.__name__)
    threads.append(t2)
    #记录问题评论到数据库的线程
    t3 = MyThread(recorder,(q1,dbpool),recorder.__name__)
    threads.append(t3)
    
    for t in threads:  
        t.start()  

