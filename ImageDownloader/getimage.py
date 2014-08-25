#encoding: utf-8
import urllib
import urllib2
import os,sys
from myThreads import MyThread
from bs4 import BeautifulSoup

class Downloader():
    def __init__(self,url):
        self.headers = {'User-agent':'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'}
        self.url = url
        self.srclist = []
        self.savepath = os.path.join(os.path.dirname(__file__),"download")
        self.request = urllib2.Request(url = self.url,headers = self.headers)
    def htmlDoc(self):
        response = urllib2.urlopen(self.request)
        return response.read()
    def download(self,htmldoc,tagname,propertyname,propertyvalue):
        soup = BeautifulSoup(htmldoc)
        list = soup.find_all(tagname,{propertyname:propertyvalue})
        for tag in list:
            self.srclist.append(tag['src'])
        return self.srclist
    def downloadImageFile(self,imgurl,filepath):
        urllib.urlretrieve(imgurl,filepath, None, None)
        
        
def main():
    print "开始解析地址：......."
    downloader = Downloader("http://triketora.tumblr.com")
    doc = downloader.htmlDoc()
    urllist = downloader.download(doc,"iframe","class","photoset") 
    Threadlist = []
    "解析出主页面中所有的iframe节点的src属性，放到列表中，在分别解析出每个iframe对应的页面中的img节点列表的src，取得图片的url"
    "为每一张图片的下载都创建一个线程，放到线程池里面"
    for url in urllist:
        imgdownloader = Downloader(url)
        imgdoc = imgdownloader.htmlDoc()
        imglist = imgdownloader.download(imgdoc, "img", "alt", "")    
        for img in imglist: 
            filename = os.path.basename(img)
            filepath = imgdownloader.savepath+"/"+filename
            t = MyThread(imgdownloader.downloadImageFile,(img,filepath),imgdownloader.downloadImageFile.__name__,filename)
            Threadlist.append(t)  
    print "解析完毕,开始启动多线程下载图片........"
    for thread in Threadlist:
        thread.start()
        thread.join() #若线程结束则退出线程，若没结束，则会阻塞该线程，知道该线程结束 
 
 
def main1():
    print "开始解析地址：......."
    d = Downloader("http://zhidao.baidu.com/link?url=D6t5CusuOMW6X6vVJHOHnp1kzmE53SuMVQnZgJH0bCAXRc9xmWu1BUef-gRuN0g_PHd7_lfwpcjKDRTaR7XVzq")
    doc = d.htmlDoc()
    list = d.download(doc, "img", "class", "ikqb_img")
    tlist = []
    for url in list:
        filename = os.path.basename(url)
        filepath = d.savepath+"/"+filename
        t = MyThread(d.downloadImageFile,(url,filepath),d.downloadImageFile.__name__,filename)
        tlist.append(t)
    print "解析完毕,开始启动多线程下载图片........"
    for thread in tlist:
        thread.start()
        thread.join()  
        
if __name__ == "__main__":
    main()
    #main1()
    
        
    
      
#     response = urllib2.urlopen("http://triketora.tumblr.com")
#     obj = BeautifulSoup(response.read())
#     print obj.prettify()       