#encoding: utf-8
from CNMThreadsGenerator import MyThread
import CNMCommentsAlarm
import CNMMessageAlarm
import CNMWeiboAlarm
import CNMDBpool
from CNMInspectUtil import TestUtil
"""将微博、评论、私信检测进程作为主进程的三个子线程，每个线程中又包含三个子线程，每个线程操作不同数据表，不会出现线程同步异常问题"""
def main():
    dbpool = CNMDBpool.InitDB()
    testutil = TestUtil(dbpool)
    main_funcs = [CNMWeiboAlarm.Weibo_main,CNMCommentsAlarm.Comment_main,CNMMessageAlarm.Sixi_main]
    main_process = []
    for func in main_funcs:
        main_process.append(MyThread(func,(dbpool,testutil),func.__name__))
    for process in main_process:
        process.start()        
    
if __name__ == "__main__":
    main()
    
    