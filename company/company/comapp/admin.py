#encoding: utf-8
from django.contrib import admin
from company.comapp.models import news,product,productSeries,info



class newsAdmin(admin.ModelAdmin):
    list_display = ('type','title','post_time')
    readonly_fields = ('thumb',) #因为不需要在后台修改该项，所以设置为只读
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields
        return self.readonly_fields

class infoAdmin(admin.ModelAdmin):
    list_display = ('type','title','post_time')
    readonly_fields = ('thumb',) #因为不需要在后台修改该项，所以设置为只读
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields
        return self.readonly_fields

    
class productAdmin(admin.ModelAdmin):
    list_display = ('name','image')
    readonly_fields = ('thumb',) #因为不需要在后台修改该项，所以设置为只读
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields
        return self.readonly_fields
class productSeriesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
    
 
    
admin.site.register(news,newsAdmin)
admin.site.register(info,infoAdmin)
admin.site.register(product, productAdmin)
admin.site.register(productSeries,productSeriesAdmin)