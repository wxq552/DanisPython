#encoding: utf-8
from __future__ import division
from django.db import models
import django.db as db
import os
import Image
from company.settings import MEDIA_ROOT,THUMB_ROOT
from django.db.models.fields.files import ImageFieldFile
# Create your models here.

def make_thumb(path, size = 480):
    pixbuf = Image.open(path)
    width, height = pixbuf.size

    if width > size:
        delta = width / size
        height = int(height / delta)
        pixbuf.thumbnail((size, height), Image.ANTIALIAS)

        return pixbuf

#定义模型管理器
class newsManager(models.Manager):
    #查询上一篇
    def getprenews(self,newsid,newstype):
        conn = db.connection
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM comapp_news c WHERE c.id<%s AND c.type=%s ORDER BY c.id DESC limit 0,1",[newsid,newstype])
        prenews = cursor.fetchone()
        return prenews
    def getafternews(self,newsid,newstype):
        conn = db.connection
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM comapp_news c WHERE c.id>%s AND c.type=%s ORDER BY c.id ASC limit 0,1",[newsid,newstype])
        prenews = cursor.fetchone()
        return prenews
    

class infoManager(models.Manager):
    #查询上一篇
    def getpreinfo(self,infoid,infotype):
        conn = db.connection
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM comapp_info c WHERE c.id<%s AND c.type=%s ORDER BY c.id DESC limit 0,1",[infoid,infotype])
        preinfo = cursor.fetchone()
        return preinfo
    def getafterinfo(self,infoid,infotype):
        conn = db.connection
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM comapp_info c WHERE c.id>%s AND c.type=%s ORDER BY c.id ASC limit 0,1",[infoid,infotype])
        preinfo = cursor.fetchone()
        return preinfo
    
       
#新闻模型
class news(models.Model):
    title = models.CharField(max_length=50,verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    post_time = models.DateField(verbose_name="发布时间")
    #img = models.CharField(verbose_name="新闻图片",max_length=20)
    image = models.ImageField(upload_to = 'big/',blank=True)
    thumb = models.ImageField(upload_to = 'big/thumb', blank = True)
    author = models.CharField(max_length=20,verbose_name="发布者")
    type = models.CharField(max_length=20,verbose_name="类型",choices=(('company','公司新闻'),('job','行业新闻'),
                                                                       ('qihuo','外盘期货')))
    objects = newsManager()
    def save(self):
        super(news, self).save() #将上传的图片先保存一下，否则报错
        if self.image:
            base, ext = os.path.splitext(os.path.basename(self.image.path))
            thumb_pixbuf = make_thumb(os.path.join(MEDIA_ROOT, self.image.name))
            relate_thumb_path = os.path.join(THUMB_ROOT, "small/"+base + '.thumb' + ext)
            thumb_path = os.path.join(MEDIA_ROOT, relate_thumb_path)
            thumb_pixbuf.save(thumb_path)
            self.thumb = ImageFieldFile(self, self.thumb, relate_thumb_path)
            super(news, self).save() 
        #再保存一下，包括缩略图等
    
    def __unicode__(self):
        return self.title
#产品系列模型
class productSeries(models.Model):
    name = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name
        
#产品模型
class product(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to = 'big/')
    thumb = models.ImageField(upload_to = 'big/thumb', blank = True)
    productseries = models.ForeignKey(productSeries)
    def save(self):
        super(product, self).save() #将上传的图片先保存一下，否则报错
        base, ext = os.path.splitext(os.path.basename(self.image.path))
        thumb_pixbuf = make_thumb(os.path.join(MEDIA_ROOT, self.image.name))
        relate_thumb_path = os.path.join(THUMB_ROOT, "small/"+base + '.thumb' + ext)
        thumb_path = os.path.join(MEDIA_ROOT, relate_thumb_path)
        thumb_pixbuf.save(thumb_path)
        self.thumb = ImageFieldFile(self, self.thumb, relate_thumb_path)
        super(product, self).save() 
        #再保存一下，包括缩略图等
        
#关于我们信息模型
class info(models.Model):
    title = models.CharField(max_length=50,verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    post_time = models.DateField(verbose_name="发布时间")
    image = models.ImageField(upload_to = 'big/',blank=True)
    thumb = models.ImageField(upload_to = 'big/thumb', blank = True)
    author = models.CharField(max_length=20,verbose_name="发布者")
    type = models.CharField(max_length=20,verbose_name="类型",choices=(('intro','公司简介'),('institute','组织机构'),
                                                                       ('range','经营范围'),('culture','企业文化'),('glory','荣誉资质'),('staff','员工天地'),('knowledge','食用油知识')))
    objects = infoManager()
    def save(self):
        super(info, self).save() #将上传的图片先保存一下，否则报错
        if self.image:
            base, ext = os.path.splitext(os.path.basename(self.image.path))
            thumb_pixbuf = make_thumb(os.path.join(MEDIA_ROOT, self.image.name))
            relate_thumb_path = os.path.join(THUMB_ROOT, "small/"+base + '.thumb' + ext)
            thumb_path = os.path.join(MEDIA_ROOT, relate_thumb_path)
            thumb_pixbuf.save(thumb_path)
            self.thumb = ImageFieldFile(self, self.thumb, relate_thumb_path)
            super(info, self).save() 
    def __unicode__(self):
        return self.title
        