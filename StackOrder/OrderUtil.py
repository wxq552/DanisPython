#encoding: utf-8
import json
import logging 
import os

class OrderUtil():
    def __init__(self,redis):
        logging.basicConfig(filename=os.path.join(os.getcwd(),"logs/log.txt"),filemode="w",
                    level=logging.DEBUG,format = '%(asctime)s - %(levelname)s: %(message)s')
        self.log = logging.getLogger("root")
        self.redis = redis
    def CheckOrder(self,order):
        order_type = order[2]
        if int(order_type) == 1:
            self.log.debug(str(order[0])+":挂单买入,股票代码："+str(order[1]))
            if self.redis.hget("rsh_stock_subspended",str(order[1])):
                self.log.debug(str(order[0])+":挂单停牌,股票:"+str(order[1])+"暂时不能买入")
            else:
                #print order[1]
                stock_snap = self.redis.hget("rsh_stock_snap",str(order[1]))
                stock_dict = json.loads(stock_snap)
                lastpx = int(stock_dict["lastpx"])
                preclosepx = int(stock_dict["preclosepx"])
                #print lastpx
                #print preclosepx
                if lastpx/10000.0 >= float(preclosepx*1.1/10000):
                    self.log.debug("股票:"+str(order[1])+"涨停,暂时不能买入")
                else:
                    return order[0]
        else:
            self.log.debug(str(order[0])+":挂单卖出,股票代码："+str(order[1]))
            if self.redis.hget("rsh_stock_subspended",str(order[1])):
                self.log.debug(str(order[0])+":挂单停牌,股票:"+str(order[1])+"暂时不能卖出")
            else:
                #print order[1]
                stock_snap = self.redis.hget("rsh_stock_snap",str(order[1]))
                stock_dict = json.loads(stock_snap)
                lastpx = int(stock_dict["lastpx"])
                preclosepx = int(stock_dict["preclosepx"])
                #print lastpx
                #print preclosepx
                if lastpx/10000.0 >= float(preclosepx*0.9/10000):
                    self.log.debug("股票:"+str(order[1])+"跌停,暂时不能卖出")
                else:
                    return order[0]
                
                
    