# Create your views here.
#encoding: utf-8
from django.http import Http404,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from MyWeibo.initClient.initClient import get_client,return_client,dump_tokens
from MyWeibo.myweibo.forms import weibodata
from django.views.decorators.csrf import csrf_exempt
import time,pymongo
import json
import os

#index
def index(request):
    access_list = []
    conn = pymongo.Connection("localhost")
    db = conn.myweibo
    access = db.access
    raw_access_list = access.find()
    for raw_access in raw_access_list:
        del raw_access["_id"]
        access_list.append(raw_access)
    conn.close()
    return render_to_response("index.html",{"access_list":access_list})

#已授权的用户登陆
def access_login(request,page=1):
    access_token= request.GET.get("access_token","")
    nickname= request.GET.get("nickname","")
    flag = get_client(access_token,nickname)
    client = return_client()
    if flag:
        data = client.statuses.home_timeline.get(page=page,count=20)
        home_list = data.statuses
        form = weibodata()
        return render_to_response("home_timeline.html",{"home_list":home_list,"page":page,
                                                        "form":form,"nickname":nickname,
                                                        "access_token":access_token})
    
    
#登陆验证授权
def login(request,page=1):
    flag = get_client()
    client = return_client()
    if flag:
        data = client.statuses.home_timeline.get(page=page,count=20)
        home_list = data.statuses
        form = weibodata()
        return render_to_response("home_timeline.html",{"home_list":home_list,"page":page,"form":form})
    #print type(client)
    return render_to_response("index.html")

#获取微博数据
def getweibo(request,page=1):
    if int(page) == 0 :
        page = 1
    client = return_client()
    form = weibodata()
    data = client.statuses.home_timeline.get(page=page,count=20)
    home_list = data.statuses
    return render_to_response("home_timeline.html",{"home_list":home_list,"page":page,"form":form,
                                                    "access_token":client.access_token,
                                                    "nickname":client.nickname})

#发布文字微博
@csrf_exempt #禁用限制跨域访问
def post_weibo(request):
    content =  request.POST["content"]
    weibo_img = request.FILES.get("weibo_img","")
    client =  return_client()
    #print content
    #print weibo_img
    if weibo_img:
        client.statuses.upload.post(status=content, pic=weibo_img)
    else:
        client.statuses.update.post(status = content)
    #time.sleep(1)
    return HttpResponseRedirect("/access_login/?access_token="+client.access_token+"&nickname="+client.nickname)


#授权回调url执行的视图函数
def get_access_token(request):
    #print request.GET['code']
    conn = pymongo.Connection("localhost")
    db = conn.myweibo
    access = db.access
    client = return_client()
    r = client.request_access_token(request.GET['code'])
    access_token = r.access_token   # 新浪返回的token，类似abc123xyz456
    expires_in = r.expires_in   # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
    print '=> the new access_token is : %s' % access_token 
    print 'access_token expires_in: ', expires_in
    #dump_tokens(access_token) 
    client.set_access_token(access_token, expires_in)
    data = client.users.show.get(uid=r.get('uid', None))
    nickname = data.screen_name
    id_pic =  data.profile_image_url
    client.access_token = access_token
    client.nickname = nickname
    access.insert({"nickname":nickname,"id_pic":id_pic,"access_token":access_token})
    conn.close()
    return HttpResponseRedirect("/access_login/?access_token="+access_token+"&nickname="+nickname)

#退出登陆，从MongoDB中删除用户认证信息
def logout(request):
    access_token = request.GET.get("access_token","")
    conn = pymongo.Connection("localhost")
    db = conn.myweibo
    access = db.access
    access.remove({"access_token":access_token})
    return HttpResponseRedirect("/")
#转发微博
@csrf_exempt #禁用限制跨域访问  
def repost(request):
    weibo_id = request.POST.get("weibo_id","")
    content = request.POST.get("content","")
    client = return_client()
    client.statuses.repost.post(id=weibo_id,status=content)
    reback = "access_token="+client.access_token+"&nickname="+client.nickname
    return HttpResponse(reback)