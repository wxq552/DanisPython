#encoding: utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse,Http404
from company.comapp.models import news,productSeries,info
from django.core.paginator import Paginator

def getnews(request,newstype="company",pagenum=1):
    news_list = news.objects.order_by('-id').filter(type=newstype)
    product_series = productSeries.objects.all()
    list_items = news_list[2:]
    #得到分页器
    paginator = Paginator(list_items,5)
    if int(pagenum)<1:
        pagenum = 1
    if int(pagenum)> paginator.num_pages:
        pagenum = paginator.num_pages
        
    list_items = paginator.page(pagenum)
    
    #print news_company
    if newstype == "company":
        title = "公司新闻"
    elif newstype == "job":
        title = "行业新闻"
    else:
        title = "外盘期货"
    return render_to_response("新闻列表.htm",{'news_list':news_list[:2],'title':title,'newstype':newstype
                                        ,'list_items':list_items,'product_series':product_series,
                                        })
    
def getdetail(request,newsid):
    newsobj = news.objects.get(id=newsid)
    product_series = productSeries.objects.all()
    #上一篇
    prenews = news.objects.getprenews(newsid,newsobj.type)
    #下一篇
    aftnews = news.objects.getafternews(newsid,newsobj.type)
    #print newsobj.title
    if newsobj.type == "company":
        title = "公司新闻"
    elif newsobj.type == "job":
        title = "行业新闻"
    else:
        title = "外盘期货"
        
    return render_to_response("新闻内容.htm",{'news':newsobj,'title':title,'product_series':product_series
                                        ,'prenews':prenews,'aftnews':aftnews,'newstype':newsobj.type})
    
    
    
#获取关于信息列表
def getinfo(request,infotype="intro",pagenum=1):
    info_list = info.objects.order_by('-id').filter(type=infotype)
    product_series = productSeries.objects.all()
    list_items = info_list[2:]
    #得到分页器
    paginator = Paginator(list_items,5)
    if int(pagenum)<1:
        pagenum = 1
    if int(pagenum)>paginator.num_pages:
        pagenum = paginator.num_pages
    list_items = paginator.page(pagenum)
    
    if infotype == "intro":
        title = "公司简介"
    elif infotype == "institute":
        title = "组织结构"
    elif infotype == "range":
        title = "经营范围"
    elif infotype == "culture":
        title = "企业文化"
    elif infotype == "glory":
        title = "荣誉资质"
    elif infotype == "staff":
        title = "员工天地"
    return render_to_response('关于列表.htm',{'info_list':info_list[:2],'title':title,
                                          'infotype':infotype,'list_items':list_items,
                                          'product_series':product_series,
                                          })
    
#关于信息详细    
def aboutdta(request,infoid):
    infobean  = info.objects.get(id = infoid)
    #获取产品系列
    product_series = productSeries.objects.all()
    #上一篇
    preinfo = info.objects.getpreinfo(infoid,infobean.type)
    #下一篇
    aftinfo = info.objects.getafterinfo(infoid,infobean.type)
    
    
    
    if infobean.type == "intro":
        title = "公司简介"
    elif infobean.type == "institute":
        title = "组织结构"
    elif infobean.type == "range":
        title = "经营范围"
    elif infobean.type == "culture":
        title = "企业文化"
    elif infobean.type == "glory":
        title = "荣誉资质"
    elif infobean.type == "staff":
        title = "员工天地"
    
    return render_to_response('关于内容.htm',{'info':infobean,'title':title,'product_series':product_series
                                          ,'preinfo':preinfo,'aftinfo':aftinfo,})
    
