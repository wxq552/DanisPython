#encoding: utf-8
import util
import csv
"""计算J值及心情指数主模块"""

if __name__ in "__main__":
    """统计J值和心情指数,生成报表Excel"""
#     with open("export.csv","wb") as csvfile:
#         spamwriter = csv.writer(csvfile,dialect='excel')
#         for i in range(0,68):
#             J = util.GetJValue(30,i)
#             INDEX = util.GetMoodIndex(21,i)
#             DATE = util.GetTradeDate(i)
#             spamwriter.writerow([J,INDEX,DATE])
    """计算J值和心情指数"""
    J = util.GetJValue(30,17)
    INDEX = util.GetMoodIndex(21,17)
    print "今天的J值：",J
    print "今天的心情指数：",INDEX   
      
    

    
    
    
    
        
    
    
    
