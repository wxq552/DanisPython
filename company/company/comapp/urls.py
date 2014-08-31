from django.conf.urls.defaults import patterns,url
from company.comapp.views import index
from company.comapp.views1 import getnews,getdetail,aboutdta,getinfo
from company.comapp.views2 import products
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'company.views.home', name='home'),
    # url(r'^company/', include('company.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
      url(r'index/$',index),
      url(r'news/$',getnews),
      url(r'infos/$',getinfo),
      url(r'infos/(?P<infotype>\w+)/$',getinfo),
      url(r'news/(?P<newstype>\w+)/$',getnews),
      url(r'news/(?P<newstype>\w+)/(?P<pagenum>\d{1,10})/$',getnews),
      url(r'detail/(?P<newsid>\d{1,10})/$',getdetail),
      url(r'infos/(?P<infotype>\w+)/(?P<pagenum>\d{1,10})/$',getinfo),
      url(r'^$',index),
      url(r'aboutdta/(?P<infoid>\d{1,10})/$',aboutdta),
      url(r'products/$',products),
      url(r'products/(?P<pro_id>\d{1,10})/$',products),
      url(r'products/(?P<pro_id>\d{1,10})/(?P<pagenum>\d{1,10})/$',products),
      
)