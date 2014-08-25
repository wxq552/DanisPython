#encoding: utf-8
from ThreadsGenerator import MyThread
import DBpool,config
from OrderUtil import OrderUtil
from time import sleep
from Queue import Queue
import urllib,urllib2,datetime,hashlib
from urllib2 import Request

def writeQ(dbpool,queue1):
    conn = dbpool.connection()
    cursor = conn.cursor()
    cursor.execute("select order_id,stock_code,order_type from ts_gs_stock_order")
    for order in cursor.fetchall():
        queue1.put(order)
    cursor.close()
    conn.close()
    
def readQ(queue1,orderutil,queue2):
    order = queue1.get(1)
    reback = orderutil.CheckOrder(order)
    if reback:
        queue2.put(reback)
    else:
        pass
            
def callApi(queue2):
    orderId = queue2.get(1)
    print orderId
    theDate = datetime.date.today()
    m = hashlib.md5(str(theDate))
    m.digest()
    safeCode = m.hexdigest()
    url = config.URLPREFIX+'/index.php?app=summary&mod=CggsTrading&act=disposeTrading'
    data = urllib.urlencode({"verification":safeCode,"orderId":orderId})
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    request = Request(url = url,data = data,headers = headers)
    #print request.get_method()
    #print data
    response = urllib2.urlopen(request)
    print response.read()    
    
#负责间隔一定时间扫描数据表，拿到挂单放到Queue中
def writer(dbpool,queue1):
    while True:
        writeQ(dbpool,queue1)
        #sleep(10)
#负责从队列中取出挂单进行过滤
def reader(queue1,orderutil,queue2):
    while True:  
        readQ(queue1,orderutil,queue2)  
        #sleep(2)  
#负责从队列中取出记录，保存到数据库      
def callwebapi(queue2):
    while True:
        callApi(queue2)
        #sleep(2)
        
def main():
    dbpool = DBpool.InitDB()
    redis = DBpool.getRedis()
    orderutil = OrderUtil(redis)
    queue1 = Queue(0)
    queue2 = Queue(0)
    threads = []
    threads.append(MyThread(writer,(dbpool,queue1),writer.__name__))
    threads.append(MyThread(reader,(queue1,orderutil,queue2),reader.__name__))
    threads.append(MyThread(callwebapi,(queue2,),callwebapi.__name__))
    for i in range(len(threads)):
        threads[i].start()
    
if __name__ == "__main__":
    main()
    
    