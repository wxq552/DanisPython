#encoding: utf-8
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
chormedriver = "C:\Documents and Settings\Administrator\Local Settings\Application Data\Google\Chrome\Application\chromedriver.exe"
#打开IE浏览器
#iedriver = "C:\Program Files\Internet Explorer\IEDriverServer.exe"
#os.environ["webdriver.ie.driver"] = iedriver
#打开谷歌浏览器
os.environ["webdriver.chrome.driver"]= chormedriver
browser = webdriver.Ie(chormedriver)
browser.maximize_window()
browser.get("http://www.51.la/")
#assert "Python" in driver.title
elem = browser.find_element_by_id("uname")
elem.send_keys(u'XXX')
elem = browser.find_element_by_id("upass")
elem.send_keys("XXXX")
browser.find_element_by_class_name("btlogin").click()

browser.implicitly_wait(5)

browser.find_element_by_link_text("查看统计报表").click()

browser.implicitly_wait(5)

browser.find_element_by_link_text("访问明细").click()

browser.implicitly_wait(5)

browser.find_element_by_link_text("压缩并下载当前报表").click()

browser.implicitly_wait(40)

browser.find_element_by_css_selector("img[alt='下载数据文件']").click()

try:
    time.sleep(30)
    browser.quit()
    sys.exit(1)
except SystemExit, value:
    print "caught exit(%s)" % value
try:
    time.sleep(20)
    browser.quit()
    os._exit(2)
except SystemExit, value:
    print "caught exit(%s)" % value
    print "bye!"



