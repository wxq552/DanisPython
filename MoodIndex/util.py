#encoding: utf-8
import math
from calculate import calculate
#SMA函数实现        
def SMA(RES_LIST,i,N,M,LIST):
    if i == 0:
        LIST.append(RES_LIST[i])
        i = i + 1
        SMA(RES_LIST,i,N,M,LIST)
    elif i == 1:
        LIST.append((M*RES_LIST[i]+(N-M)*LIST[-1])/N)
        i = i + 1
        SMA(RES_LIST,i,N,M,LIST)
    elif i == N:
        return
    else:
        LIST.append((M*RES_LIST[i]+(N-M)*LIST[-1])/N)
        i = i + 1
        SMA(RES_LIST,i,N,M,LIST)
        
#计算J值
def GetJValue(N,day):
    KLIST = [] #存放K值的列表
    RSV_LIST = []  #存放RSV值的列表
    DLIST = []  #存放D值的列表
    c = calculate(N,day)  
    highlist = c.GetHighpxList()
    lowlist = c.GetLowhpxList()
    HHV = c.HHV(highlist)
    LLV = c.LLV(lowlist)
    #计算最近5天内的RSV值 
    for i in range(4,-1,-1):
        #print i
        RSV_LIST.append(c.RSV(c.GetClosepx(i),LLV,HHV))
    #计算K值
    i = 0
    j = 0
    SMA(RSV_LIST,i,5,1,KLIST)
    SMA(KLIST[2:],j,3,1,DLIST)    
    K = KLIST[-1]
    D = DLIST[-1]
    J = 3*K-2*D
    return J     
#计算心情指数   
def GetMoodIndex(N,day):
    AA4_LIST = [] #存放AA4数据的列表
    AA5_LIST = [] #存放AA5数据的列表
    AA6_LIST = []
    c = calculate(N,day)
    highlist = c.GetHighpxList()
    lowlist = c.GetLowhpxList()
    HHV = c.HHV(highlist)
    LLV = c.LLV(lowlist)
    for i in range(12,-1,-1):
        AA4_LIST.append(c.RSV(c.GetClosepx(i), LLV, HHV))
    #计算最近心情指数
    i = 0
    j = 0
    SMA(AA4_LIST,i,13,8,AA5_LIST)
    SMA(AA5_LIST,j,13,8,AA6_LIST)
    INDEX = math.ceil(AA6_LIST[-1])
    return INDEX
#获取日期
def GetTradeDate(i):
    c = calculate()
    return c.tradedate[i]
    