import MySQLdb
import re
conn = MySQLdb.connect(host='localhost',user='root',passwd='root',db='test',charset='utf8')
cursor = conn.cursor()
file = open("data.txt","r")
pattern = r'\t*'
for line in reversed(file.readlines()):
    list = re.split(pattern,line)[0:5]
    print list    
    sql = "insert into testdata (tradedate,openpx,highpx,lowpx,closepx) values (%s,%s,%s,%s,%s)"
    cursor.execute(sql,list)
conn.commit()

cursor.close()
conn.close()