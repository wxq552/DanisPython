# Create your views here.
#encoding: utf-8
from django.http import Http404,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from MyWeibo.initClient.initClient import get_client,return_client,dump_tokens
from MyWeibo.myweibo.forms import weibodata
import urllib
from django.views.decorators.csrf import csrf_exempt
import time,os,json

def getcomments(request,weibo_id,page=1):
    client = return_client()
    #print weibo_id
    comments = client.comments.show.get(id=weibo_id,page = page)
    comments_list = comments.comments
    #json模块提供了用于将字典转换为json的方法
    return  HttpResponse(json.dumps(comments_list))
@csrf_exempt
def post_comment(request):
    weibo_id = request.POST.get("wid","")
    comm_id = request.POST.get("cid","")
    comms =  request.POST.get("data","")
    client = return_client()
    client.comments.reply.post(id=weibo_id,cid=comm_id,comment=comms)
    comments = client.comments.show.get(id=weibo_id,page = 1)
    comments_list = comments.comments
    return HttpResponse(json.dumps(comments_list));
    
        
    