from django.contrib import admin
from web import models
# Register your models here.


class WebContentInfo(admin.ModelAdmin):
    list_display = ('title','content_auth','content')

class UserTypeInfo(admin.ModelAdmin):
    list_display = ("id","typename")
    
class CommentInfo(admin.ModelAdmin):
    list_display = ("comment_content","comment_user")
    
class ContactInfo(admin.ModelAdmin):
    list_display = ("contact_content","contact_user")
    
class ContenttypeInfo(admin.ModelAdmin):
    list_display = ("id","typename")

    
admin.site.register(models.Comment,CommentInfo)
admin.site.register(models.Contact,ContactInfo)
admin.site.register(models.ContentType,ContenttypeInfo)
admin.site.register(models.UserInfo,)
admin.site.register(models.UserType,UserTypeInfo)
admin.site.register(models.WebContent,WebContentInfo)