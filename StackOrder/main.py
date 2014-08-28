#encoding: utf-8
from ThreadsGenerator import MyThread
import DBpool,config
from OrderUtil import OrderUtil
from time import sleep
from Queue import Queue
import urllib,urllib2,datetime,hashlib
from urllib2 import Request
import time
#扫描挂单,扫描未处理状态的挂单
current_open = time.time() #获取开盘时间
print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(current_open))
def writeQ(dbpool,queue1):
    global current_open
    begin_time = time.time()-60
    print "当前的时间:"+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(begin_time))
    conn = dbpool.connection()
    cursor = conn.cursor()
    cursor.execute("select order_id,stock_code,order_type,order_iscancel from ts_gs_stock_order where order_status = 1 and order_ctime >= %s and order_ctime <= %s",
                   [current_open,begin_time])
    #cursor.execute("select order_id,stock_code,order_type,order_iscancel,order_price from ts_gs_stock_order where order_status = 1")
    for order in cursor.fetchall():
        #设置挂单为正在处理中状态
        if int(order[3]) == 0:
            cursor.execute("update ts_gs_stock_order set order_status = 2 where order_id = %s",[order[0]])
            queue1.put(order)
    cursor.close()
    conn.close()
#检查挂单记录
def readQ(queue1,orderutil,queue2):
    order = queue1.get(1)
    reback = orderutil.CheckOrder(order)
    if reback:
        print reback
        queue2.put(reback) #检查挂单可以交易（非停牌非涨跌停）
    else:
        queue1.put(order)  #暂时不能交易的挂单要继续扫（停牌涨跌停状态）
#调用web接口对可以交易的挂单进行成交处理
def callApi(queue2,dbpool,queue1):
    conn = dbpool.connection()
    cursor  = conn.cursor()
    orderId = queue2.get(1)
    theDate = datetime.date.today()
    m = hashlib.md5(str(theDate))
    m.digest()
    safeCode = m.hexdigest()
    url = config.URLPREFIX+'/index.php?app=cggs&mod=CggsTrading&act=disposeTrading'
    data = urllib.urlencode({"verification":safeCode,"orderId":orderId})
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    request = Request(url = url,data = data,headers = headers)
    response = urllib2.urlopen(request)
    result = response.read() #将queue2中可以交易的挂单调用web接口进行成交处理
    #print result
    if int(result) == 1:
        print orderId
        cursor.execute("update ts_gs_stock_order set order_status = 3 where order_id = %s",[orderId]) #挂单处理成功，设置为已处理状态
    else:
        cursor.execute("select order_id,stock_code,order_type,order_iscancel,order_price from ts_gs_stock_order where order_id = %s",[orderId]) #成交处理失败，在行进处理
        order = cursor.fetchone()
        queue1.put(order)
    cursor.close()
    conn.close()
    
#负责间隔一定时间扫描数据表，拿到挂单放到Queue中
def writer(dbpool,queue1):
    while True:
        writeQ(dbpool,queue1)
        #sleep(5)
#负责从队列中取出挂单进行检查
def reader(queue1,orderutil,queue2):
    while True:  
        readQ(queue1,orderutil,queue2)  
        #sleep(2)  
#负责从队列中取出记录，保存到数据库      
def callwebapi(queue2,dbpool,queue1):
    while True:
        callApi(queue2,dbpool,queue1)
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
    threads.append(MyThread(callwebapi,(queue2,dbpool,queue1),callwebapi.__name__))
    for i in range(len(threads)):
        threads[i].start()
    
if __name__ == "__main__":
    main()
    
    