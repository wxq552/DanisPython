流量IP数统计自动化处理程序
包括自动下载流统计表程序和自动统去重Ip数程序

需要先安装python selenium自动化测试框架
在谷歌浏览器安装目录C:\Documents and Settings\Administrator\Local Settings\Application Data\Google\Chrome\Application\
下放置chromedriver.exe

使用：download.py用于在www.51la.com下载流量统计报表(需要填写用户名密码登陆)
      counter.py用于分析计算每天下载的流量表中的去重ip数，及时计算过去一周内及一个月内的去重ip数，并记录在日志中。
需要使用MongoDB数据库，使用Windows任务调度器可以实现自动化。
