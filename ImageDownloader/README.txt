爬虫程序，图片抓取器，抓取http://triketora.tumblr.com/
博客网站的图片
使用BeautifulSoup解析出图片url,对每一张图片的下载都开启一个线程负责，
将多个线程放到线程池，并用join来阻塞进程直至所有线程执行完毕。
