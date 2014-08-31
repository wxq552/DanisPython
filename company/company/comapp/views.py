#encoding: utf8
# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse,Http404
import os
from company.comapp.models import news,product,productSeries,info
def index(request):
    
    #公司新闻
    news_company = news.objects.order_by('-id').filter(type="company")[:5]
    if news_company: 
        firstcompany = news_company[0]
    else:
        firstcompany = None
    
    #行业新闻
    news_job = news.objects.order_by('-id').filter(type="job")[:5]
    if news_job:
        firstjob = news_job[0]
    else:
        firstjob = None
        
    #外盘期货
    news_qihuo = news.objects.order_by('-id').filter(type="qihuo")[:5]
    
    #员工天地
    staff_list = info.objects.order_by('-id').filter(type="staff")[:5]
    #食用油知识
    knowledge_list = info.objects.order_by('-id').filter(type="knowledge")[:5]
    #公司简介
    intro =  info.objects.order_by('-id').filter(type="intro")[0]
    #print news_list
    #产品列表
    product_list = product.objects.order_by('-id')
    #产品系列
    product_series = productSeries.objects.all()
    return render_to_response("index.html",{'news_company':news_company,'firstcompany':firstcompany
                                            ,'news_job':news_job,'firstjob':firstjob
                                            ,'news_qihuo':news_qihuo,'news_qihuo':news_qihuo,
                                            'product_list':product_list,'product_series':product_series,
                                            'staff_list':staff_list,'knowledge_list':knowledge_list,
                                            'intro':intro,
                                            })
    
    
    
    


    