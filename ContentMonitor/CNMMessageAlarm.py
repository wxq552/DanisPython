#encoding: utf-8
from CNMThreadsGenerator import MyThread
from time import sleep
from Queue import Queue
import time
import logging
import os
delay = 0
logging.basicConfig(filename=os.path.join(os.getcwd(),"log.txt"),filemode="w",
                    level=logging.DEBUG,format = '%(asctime)s - %(levelname)s: %(message)s')
log = logging.getLogger("root.log3")
ALARM_LEVEL1 = 1 #"黄图嫌疑，敏感词嫌疑"
ALARM_LEVEL2 = 2 #"黄图嫌疑"
ALARM_LEVEL3 = 3 #"敏感词嫌疑"
#实现每间隔1分钟扫描私信表获取最近一分钟发表的私信列表，并加到队列中
def writeQ(queue,dbpool):  
    global delay
    begin_time = time.time()-delay-60
    now = time.time()-delay
    local_begin_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(begin_time))
    local_now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(now))
    log.debug('开始扫描私信列表,并加入最近一分钟新发表的私信到队列中')
    log.debug("一分钟之前时间：%s",*(local_begin_time,))
    log.debug("当前时间：%s",*(local_now,))
    conn = dbpool.connection()
    cursor = conn.cursor()
    #cursor.execute("select message_id,list_id,from_uid,content,is_del,mtime from ts_message_content where mtime>=%s and mtime<=%s",[begin_time,now])# order by message_id desc limit 0,5")
    cursor.execute("select message_id,list_id,from_uid,content,is_del,mtime from ts_message_content order by message_id desc limit 0,5") 
    sx_list = cursor.fetchall()
    cursor.close()
    conn.close()
    delay = len(sx_list)
    for wb in sx_list:
        #print wb[5]
        if int(wb[4]) == 0: 
            queue.put(wb,1) 
    delay = time.time()-now #执行语句延迟了的时间，补回来，回到原来的时间点
#实现从队列中读取每一条私信，识别私信的图片及敏感词，若有问题，则将记录加入到队列中
def readQ(queue,queue1,testutil):  
    val=queue.get(1)  
    log.debug('从队列中取出一条私信出来检测')#队列长度为：',queue.qsize()
    if testutil.ContainBanWord(val[3]):
        record = [val[0],val[1],val[2],val[5],ALARM_LEVEL3]
        queue1.put(record,1)
        log.debug("敏感词嫌疑！！！")
    else:
        log.debug("私信健康！！！")
#实现从队列中获取记录存储到数据库中
def addtoTable(queue1,dbpool):
    val = queue1.get(1)
    sql = "insert into ts_mb_iffy_message (message_id,list_id,from_uid,mtime,reason) values (%s,%s,%s,%s,%s)"
    conn = dbpool.connection()
    cursor = conn.cursor()
    cursor.execute(sql,val)
    conn.commit()
    cursor.close()
    conn.close()
    log.debug("已记录到的一条问题私信")
#负责间隔一定时间扫描数据表，拿到私信数据放到Queue中
def writer(queue,dbpool):
    while True:
        writeQ(queue,dbpool)
        sleep(60)

#负责从队列中取出私信进行过滤识别
def reader(queue,queue1,testutil):
    while True:  
        readQ(queue,queue1,testutil)  
        sleep(1)  
#负责从队列queue1中取出记录，保存到数据库        
def recorder(queue1,dbpool):
    while True:
        addtoTable(queue1,dbpool)
        sleep(1)
    
def Sixi_main(dbpool,testutil):   
    q=Queue(0)
    q1 = Queue(0)  
    threads=[]  
       
    #扫描私信的线程
    t1 = MyThread(writer,(q,dbpool),writer.__name__)
    threads.append(t1)
    #识别过滤的线程
    t2 = MyThread(reader,(q,q1,testutil),reader.__name__)
    threads.append(t2)
    #记录问题私信到数据库的线程
    t3 = MyThread(recorder,(q1,dbpool),recorder.__name__)
    threads.append(t3)
    
    for t in threads:  
        t.start()  

