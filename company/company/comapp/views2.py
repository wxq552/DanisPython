#encoding: utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse,Http404
from company.comapp.models import productSeries
from django.core.paginator import Paginator
#产品列表
def products(request,pro_id = 0,pagenum=1):
    product_series = productSeries.objects.all()
    if pro_id == 0:
        #默认产品系列
        current_series = product_series[0]
        #获取默认产品系列下的产品列表
        products = current_series.product_set.all()
    if pro_id == 0:
        title = current_series.name
    else:
        current_series = productSeries.objects.get(id = pro_id)
        products = current_series.product_set.all()
        title =  current_series.name
    
    paginator = Paginator(products,8)
    if int(pagenum)<1: 
        pagenum = 1
    if int(pagenum)> paginator.num_pages:
        pagenum = paginator.num_pages
    item_list = paginator.page(pagenum)
    return render_to_response('产品列表.htm',{'item_list':item_list,'title':title,
                                          'product_series':product_series,'current_series':current_series})
    