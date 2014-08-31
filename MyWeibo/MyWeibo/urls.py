from django.conf.urls.defaults import patterns, include, url
from MyWeibo.myweibo.views import index,login,get_access_token,getweibo,post_weibo,access_login,logout,repost
from MyWeibo.myweibo.view1 import getcomments,post_comment
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MyWeibo.views.home', name='home'),
    # url(r'^MyWeibo/', include('MyWeibo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$',index),
    url(r'^access_login/$',access_login),
    url(r'^auth_login/$',login),
    url(r'^get_access_token/$',get_access_token),
    url(r'^getweibo/(?P<page>\d{1,10})/$',getweibo),
    url(r'^post_weibo/$',post_weibo),
    url(r'^getcomments/(?P<weibo_id>\d+)/$',getcomments),
    url(r'^post_comment/$',post_comment),
    url(r'^logout/$',logout),
    url(r'^repost/$',repost)
)
