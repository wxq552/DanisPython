import MySQLdb
import os
import redis
from DBUtils.PooledDB import PooledDB
config = {}
execfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.py"), config)
def InitDB():
    dbpool = PooledDB(creator=MySQLdb,mincached=10,maxusage=10,host=config['HOST'],
                      user=config['USERNAME'],passwd=config['PASSWORD'],db=config['DBNAME'],
                      charset=config['CHARSET'],port=config['PORT'])
    return dbpool

def getRedis():
    r = redis.StrictRedis(host='192.168.100.1', port=6379, db=0)
    return r