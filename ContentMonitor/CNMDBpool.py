import MySQLdb
import os
from DBUtils.PooledDB import PooledDB
config = {}
execfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "CNMconfig.py"), config)
def InitDB():
    dbpool = PooledDB(creator=MySQLdb,mincached=100,maxusage=100,host=config['HOST'],
                      user=config['USERNAME'],passwd=config['PASSWORD'],db=config['DBNAME'],
                      charset=config['CHARSET'],port=config['PORT'])
    return dbpool
# if __name__ == "__main__":
#     dbpool = InitDB()
#     conn = dbpool.connection(True)
#     cursor = conn.cursor()
#     cursor.execute("select * from ts_weibo limit 0,10")
#     print cursor.fetchall()