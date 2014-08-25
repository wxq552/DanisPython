#encoding: utf-8
from PIL import Image  
import smallgfw
class TestUtil():
    def __init__(self,dbpool):
        self.conn = dbpool.connection()
        self.cursor = self.conn.cursor()
        self.cursor.execute("select sensitive_word from ts_mb_sensitive")
        self.banwords = self.cursor.fetchall()
        self.cursor.close()
        self.conn.close()

    def IspornImage(self,imgurl):
        img = Image.open(imgurl).convert('YCbCr')  
        w, h = img.size  
        data = img.getdata()  
        cnt = 0  
        for i, ycbcr in enumerate(data):  
            y, cb, cr = ycbcr  
            if 86 <= cb <= 117 and 140 <= cr <= 168:  
                cnt += 1  
        if cnt > w * h * 0.3:
            return True
        else:
            return False 
    def GetBanword(self):
        return list(self.banwords)
    def ContainBanWord(self,wb_text):
        banlist = [] #敏感词列表
        for ban in self.GetBanword():
            banlist.append(ban[0])
        gfw = smallgfw.GFW()
        gfw.set(banlist)#设置敏感词列表
        resultlist = gfw.check(wb_text)
        if resultlist:
            return True
        else:
            return False
        
        
    
        
        