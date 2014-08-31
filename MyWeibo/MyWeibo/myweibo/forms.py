#encoding: utf-8
from django import forms

class weibodata(forms.Form):
    content = forms.CharField(widget=forms.Textarea,label="") 
    weibo_img = forms.FileField(label="")
    
    