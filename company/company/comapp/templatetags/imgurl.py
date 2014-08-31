from django import template
import os
register = template.Library()
def imgurl(value):
    imgurl = os.path.basename(value)
    #print imgurl
    return imgurl
register.filter('imgurl',imgurl)