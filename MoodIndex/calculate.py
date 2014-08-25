#encoding: utf-8
import MySQLdb
class calculate():
    def __init__(self,N=30,day=0):
        self.conn = MySQLdb.connect(host='localhost',user='root',passwd='root',db='test',charset='utf8')
        self.cursor = self.conn.cursor()        
        self.N = N
        self.day = day
        self.cursor.execute("select closepx from testdata")
        self.closepx = []
        for item in self.cursor.fetchall():
            self.closepx.append(float(item[0]))
        self.CLOSE_LIST = self.closepx[self.day:self.N+self.day]
        self.cursor.execute("select tradedate from testdata")
        self.tradedate = []
        for item in self.cursor.fetchall():
            self.tradedate.append(str(item[0]))
        
        #print len(self.CLOSE_LIST)
    def getconn(self):
        self.conn = MySQLdb.connect(host='localhost',user='root',passwd='root',db='test',charset='utf8')
        self.cursor = self.conn.cursor() 
    def GetHighpxList(self):
        if self.conn is None:
            self.getconn()
        self.cursor.execute("select highpx from testdata")
        highpx = []
        for item in self.cursor.fetchall():
            highpx.append(float(item[0]))
        return highpx[self.day:self.N+self.day]
    
    def GetLowhpxList(self):
        if self.conn is None:
            self.getconn()
        self.cursor.execute("select lowpx from testdata")
        lowpx = []
        for item in self.cursor.fetchall():
            lowpx.append(float(item[0]))
        return lowpx[self.day:self.N+self.day]
    #获取每一天收盘价
    def GetClosepx(self,i):
        return self.CLOSE_LIST[i]
    #计算N周期内的最低价
    def LLV(self,lowlist):
        return min(lowlist)
    #计算N周期内的最高价
    def HHV(self,highlist):
        return max(highlist)
    #计算每一天的RSV数值
    def RSV(self,CLOSE,LLV,HHV):
        return (CLOSE-LLV)/(HHV-LLV)*100