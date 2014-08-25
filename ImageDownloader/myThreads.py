#encoding: utf-8
''''' 
Created on 2014-07-23 
@author: Administrator 
'''  
import threading  
from time import ctime  
class MyThread(threading.Thread):  
    def __init__(self,func,args,name='',filename=''):  
        threading.Thread.__init__(self)  
        self.name=name  
        self.func=func  
        self.args=args
        self.filename = filename  
    def getResult(self):  
        return self.res  
    def run(self):  
        print '开始下载文件：'+self.filename,'At:',ctime()  
        self.res=apply(self.func,self.args)  
        print '下载文件：'+self.filename+"结束",'At:',ctime()  