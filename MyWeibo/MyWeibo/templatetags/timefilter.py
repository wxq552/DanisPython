from django import template
import os,time
register = template.Library()
def timefilter(value):
    timelist = value.split(" ")
    daylist = timelist[3].split(":")
    print daylist
    #print imgurl
    print timelist
#register.filter('imgurl',imgurl)
timefilter("Sun Jul 13 09:55:52 +0800 2014")