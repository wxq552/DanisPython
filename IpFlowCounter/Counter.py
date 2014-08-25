#encoding: utf-8
import glob,re,os,stat,pymongo,zipfile,time,sys
log = open("ip_log_day.log","a+")
conn = pymongo.Connection("localhost",27017)
db = conn.ipcounter
collection = db.ipcollection
pattern = r'(\d+)\.(\d+)\.(\d+)\.(\d+)'
datepattern = r'(\d{4}-\d{1,2}-\d{1,2})'
#扫描所有的文件，获取每个文件的创建时间，与文件名组成键值对，key：文件名，value：创建时间  存放到字典中
ctime_idct = {}
for cur_file in glob.glob("*.zip"):
    ctime_idct[cur_file] = os.stat(cur_file)[stat.ST_CTIME]
    
#对字典进行排序
ctime_idct = sorted(ctime_idct.iteritems(),key = lambda asd:asd[1],reverse = True)
#print ctime_idct
#取出最新创建的文件名
latest = ctime_idct[0][0]
print latest
filename , ext = os.path.splitext(latest)
taday = filename[filename.find("-")+1:filename.rfind(" ")] 
#zip压缩文件中的文件名列表
z = zipfile.ZipFile(latest, 'r')
namelist = z.namelist()
tadayfile = z.open(namelist[0],"r")
for line in tadayfile:
    doc = {}
    line = tadayfile.readline()
    li_list = re.search(pattern,line)
    date_list = re.search(datepattern, line)
    
    if li_list and date_list:
        ip = ".".join(list(li_list.groups()))
        date = date_list.group()
        timeArray = time.strptime(date,"%Y-%m-%d")
        date = int(time.mktime(timeArray))
        doc["ip"] = ip
        doc["date"] = date
        
        #print doc
        collection.insert(doc)
    else:
        break
time.sleep(3)    
#计算今天的timestamp
timeArray = time.strptime(taday,"%Y-%m-%d")
timeStamptaday = int(time.mktime(timeArray))
#查询数据集中ip键的值不重复的ip数,写入日志文件

log.write(taday+"的去重ip数:"+str(len(collection.find({"date":timeStamptaday}).distinct("ip")))+"\n")

time.sleep(3)

# timeArray = time.strptime("2014-7-14", "%Y-%m-%d")
# timeStamp = int(time.mktime(timeArray))

#计算7天前的timestamp
weekBeforetimestamp = timeStamptaday-6*24*60*60
#计算30天前的timestamp
monthBeforetimestamp = timeStamptaday-29*24*60*60

weekbefore =  time.localtime(weekBeforetimestamp)
weekday = time.strftime("%Y-%m-%d",weekbefore)
monthbefore =  time.localtime(monthBeforetimestamp)
monthday = time.strftime("%Y-%m-%d",monthbefore)
#print time.strftime("%Y-%m-%d",int(monthBeforetimestamp))
weekcount = collection.find({"date":weekBeforetimestamp}).count()
monthcount = collection.find({"date":monthBeforetimestamp}).count()
#判断是否已满一个星期
if int(weekcount) != 0:
    weekdistinct = len(collection.find({"date":{"$gte" : weekBeforetimestamp,"$lte":timeStamptaday}}).distinct("ip"))
    log.write("================================"+str(weekday)+"至"+str(taday)+"一周内的去重ip数："+str(weekdistinct)+"================================\n")
#判断是否已满一个月
if int(monthcount) != 0:
    monthdistinct = len(collection.find({"date":{"$gte" : monthBeforetimestamp,"$lte":timeStamptaday}}).distinct("ip"))
    log.write("================================"+str(monthday)+"至"+str(taday)+"一个月内的去重ip数："+str(monthdistinct)+"================================\n")
    #print str(monthdistinct)
    



#print time.localtime(monthBeforetimestamp)
# print time.strftime("%Y-%m-%d",int(monthBeforetimestamp))
#print timeStamptaday
#print timeStamp

#print (timeStamptaday-timeStamp)/(24*60*60)

# if (timeStamptaday-timeStamp)/(24*60*60) == 7:
#     #print (timeStamptaday-timeStamp)/(24*60*60)
#     #print "aaa"
#     log.write("=================================\n本周去重ip数为："+str(len(collection.distinct("ip")))+"\n=================================\n")
# if (timeStamptaday-timeStamp)/(24*60*60) == 30:
#     log.write("=================================\n本月去重ip数为："+str(len(collection.distinct("ip")))+"\n=================================\n")
log.close()    
conn.close()
time.sleep(2)
sys.exit()
