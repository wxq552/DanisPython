import MySQLdb
conn = MySQLdb.connect(host='localhost',user='root',passwd='root',db='test',charset='utf8')
cursor = conn.cursor()
for