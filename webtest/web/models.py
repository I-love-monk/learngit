from django.db import models
from django import forms
# Create your models here.
class Form(forms.Form):
    image = forms.ImageField()
    eamil = forms.EmailField()#error_messages={"invalid":"邮箱格式不正确"}

    def __unicode__(self):
        return self.image
    


class UserType(models.Model):
    typename = models.CharField(max_length=50)
    def __unicode__(self):
        return self.typename
    class Meta:
        verbose_name_plural = "UserType"
    


class UserInfo(models.Model):
    
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=250)
    eamil = models.EmailField(unique=True)
    create_date = models.DateTimeField(auto_now_add =True)
    
    usertype = models.ForeignKey("UserType")

    
    class Meta:
        verbose_name_plural = "UserInfo"


class WebContent(models.Model):
    
    image = models.ImageField(upload_to="images",default="/static/images/timthumb.png")
    content = models.TextField()
    title = models.CharField(max_length=250)
    content_auth = models.CharField(max_length=50)
    user = models.ForeignKey("UserInfo")
    create_date = models.DateTimeField(auto_now_add =True)
    
    favor_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    click_count = models.IntegerField(default=0)
    
    contenttype = models.ForeignKey("ContentType")
    
    class Meta:
        verbose_name_plural = "WebContent"
    
class ContentType(models.Model):
    typename = models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural = "ContentType"
    
class Comment(models.Model):
    
    comment_content = models.TextField()
    comment_for = models.ForeignKey("WebContent")
    comment_favor = models.IntegerField(default=0)
    comment_user = models.ForeignKey("UserInfo")
    
    create_date = models.DateTimeField(auto_now_add =True)
    class Meta:
        verbose_name_plural = "Comment"
    
class Contact(models.Model):
    
    contact_content = models.TextField()
    contact_favor = models.IntegerField(default=0)
    contact_user = models.ForeignKey("UserInfo")    
    create_date = models.DateTimeField(auto_now_add =True)
    
    class Meta:
        verbose_name_plural = "Contact"

    
    
    
    