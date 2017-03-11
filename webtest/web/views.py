from django.contrib.auth.hashers import make_password, check_password
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template.context import RequestContext
from web import models
import json
from web import page_helper
from web.page_helper import CJenoder
from django.utils.safestring import mark_safe
import re
from web.template_helper import helper
from django import forms
from django.conf import settings
from django.core.mail import send_mail
import base64
from django.contrib import auth
from email._header_value_parser import Domain
#from web.models import ImageForm
#from PIL import Image,ImageDraw,ImageFont
#import string, random
#import io,os
#from webtest.settings import BASE_DIR

# Create your views here.
def checklogin(main_func):
    
    def _deco(request,*arg,**kwargs):
        if not request.session.get('current_user_id'):
            return redirect("/login/",RequestContext(request))
        return main_func(request,*arg,**kwargs)
    return _deco

'''
def first(request):
    return render(request,"index.html")

#pytho3.4不能运行 2.7可以----------
def captcha(request):
    size = (100,36)
    image = Image.new("RGB",size,color=(255,255,255))
    font=ImageFont.load_default().font
    #font = ImageFont.truetype(font_file, 18)
    draw = ImageDraw.Draw(image)
    rand_str = ''.join(random.sample(string.ascii_letters+string.digits,4))

    draw.text((7,0),rand_str,fill=(0,0,0),font=font)
    width,height = size
    start = (random.randint(0,width),random.randint(0,height))
    end = (random.randint(0,width),random.randint(0,height))
    draw.line([start,end],fill=(255,0,0))
    del draw
    request.session["captcha"] = rand_str.lower()
    #buf = io.StringIO()
    for i in range(10):
        yield i
    image_id = str(i)+".png"
    img = image.save("1.png","PNG")
    return HttpResponse(img)



def captcha(request):
    image = Image.new("RGB",(120,36),color=(255,255,255))#create a place
    font_file = "static/assets/fonts/fontawesome-webfont.ttf" #font file
    font = ImageFont.truetype(font_file, 36) #font style
    draw = ImageDraw.Draw(image,) #draw pen
    rand_str = ''.join(random.sample(string.ascii_letters+string.digits,4))#random string
    draw.text((17,0),rand_str,fill=(0,0,0),font=font)
    del draw
    request.session["captcha"]=rand_str.lower()
    buf = cStringIO()
    image.save(buf,"PNG")
    return HttpResponse(buf.getvalues(),"image/PNG")
'''    
                
def login(request):
    context = {"message":"","user":""}     
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        #print(password)
        temp = all([username,password])
        user = models.UserInfo.objects.filter(username=username)
        #print(user)
        if temp:
            if user:
                try:
                    pwd = models.UserInfo.objects.filter(username = username).values("password")
                    pwd = pwd[0]["password"]
                    #print(pwd)
                    result = check_password(password,pwd)
                    #print(result)
                except Exception as e:
                    print(e)
                    result = None
                if result:
                    request.session["current_user_id"]=models.UserInfo.objects.filter(username = username).values("id")[0]["id"]
                    #print(request.session["current_user_id"])
                    context["user"] = username
                    return redirect("/index/")
                    '''
                    response.set_cookie("username",username)
                    return response
                    '''
                else:
                    context["message"]="用户名或密码错误" 
            else:
                context["message"]="用户名不存在"      
        else:
            context["message"]="用户名或密码为空"
    else:
        return render_to_response("login.html", context)
            #return response
    return render_to_response("index.html", context)

def logout(request):
    auth.logout(request)
    return redirect("/index/")


class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    email = forms.EmailField()
    def __unicode__(self):
        return self.username  
    
from itsdangerous import URLSafeTimedSerializer as utsr
import base64
import re
from django.conf import settings as django_settings

class Token:
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.encodestring(security_key.encode())
    def generate_validate_token(self, username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)
    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)
    def remove_validate_token(self, token):
        serializer = utsr(self.security_key)
        print(serializer.loads(token, salt=self.salt))
        return serializer.loads(token, salt=self.salt)

token_confirm = Token(django_settings.SECRET_KEY)    # 定义为全局变量 

def register(request):
    ret={"message":''}
    if request.method == "POST":
        form = RegisterForm(request.POST)
        try:
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                email = form.cleaned_data.get("email")
                pwd = make_password(password)
                if not models.UserInfo.objects.filter(username=username): 
                #print(username,password,email)
                    user = models.UserInfo.objects.create(username=username,
                                                           password=pwd,
                                                           #email=email,
                                                           usertype=models.UserType.objects.get(id=2),
                                                           )
                    user.is_active=False
                    user.save()
                    
                    token = token_confirm.generate_validate_token(username)

                    message = "\n".join([u'{0},欢迎加入我的博客'.format(username), u'请访问该链接，完成用户验证:', 
                                                '/'.join(["http://182.61.25.152",'activate',token])])
                    send_mail('tongzhi',message,'ilovemonk@126.com',[email],fail_silently=False)

                    #print(userobj)
                    ret["message"]="注册成功，请登陆邮箱激活。" 
                    render_to_response("register.html",ret)  
                else:
                    ret["message"] = "该用户名已注册，请换一个。"
        except Exception as e:
            print(e)
            ret["message"]="系统出错了。"
        return render_to_response("register.html",ret)
    return render_to_response("register.html")   

'''

#邮箱验证
def register(request):
    ret = {"message":''}
    if request.method =="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")
            
            user = models.UserInfo.objects.create(username=username,
                                           password=password,
                                           #email=email
                                           usertype=models.UserType.objects.get(id=2)
                                           )
            user.is_active=False
            user.save()
            token = username
            message = '\n'.join(["{0} welcome".format(username),'please check email','/'.join(["active",token])])
            send_mail('tongzhi',message,'ilovemonk@126.com',[email],fail_silently=False)
            return render(request,'message.html',{"form":form})
        else:
            ret['message'] = '格式有误，请重新输入'
    return render_to_response('register.html',ret)
'''    
def active_user(request, token):
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        username = token_confirm.remove_validate_token(token)
        models.UserInfo.objects.filter(username=username).delete()
        return render(request, 'message.html', {'message': u'对不起，验证链接已经过期，请重新注册'})
    try:
        user = models.UserInfo.objects.get(username=username)
    except models.UserInfo.DoesNotExist:
        return render(request, 'message.html', {'message': u"对不起，您所验证的用户不存在，请重新注册"})
    user.is_active = True
    user.save()
    message = u'验证成功，请进行登录操作'
    return render(request, 'message.html', {'message':message})

def index(request,page):
    ret = {
            "message":'',"data":'',
            "page_list":'',"content":"",
           "user":"",
           }

    try:
        page = page_helper.checkint(page)
        #print(page)
        all_count = models.WebContent.objects.all().count()
        result = page_helper.pagerange(all_count, page,)
        #print(result)
        all_page = result[2]
        #print(all_page)
        page_list = page_helper.pagelist(page, all_page)
        contentobj = models.WebContent.objects.all().order_by("-id")[result[0]:result[1]]
        #content = mark_safe(contentobj[0].content)
        #ret["content"] = content
        ret["data"] = contentobj
        ret["status"] = 1
        ret["page_list"] = page_list
        #print(page_list)
    except Exception as e:
        ret["message"] = e
        print(e)
    
    return render_to_response("index.html",ret)

def index_type(request,type_id,page):
    ret = {
            "message":'',"data":'',
            "page_list":'',"content":"",
           "user":"",
           }
    path = request.get_full_path().split("/")
    print(path)

    try:
        page = page_helper.checkint(path[3])
        print(page)
        print(path[2])
        if int(path[2]) == 0:
            all_count = models.WebContent.objects.filter(contenttype__id__lt=3).count()
            print(all_count)
            result = page_helper.pagerange(all_count, page,)
            print(result)
            contentsobj = models.WebContent.objects.filter(contenttype__id__lt=3).order_by("-id")[result[0]:result[1]]
        elif int(path[2]) == 6:
            all_count = models.WebContent.objects.filter(contenttype__id__gt=2).count()
            print(all_count)
            result = page_helper.pagerange(all_count, page,)
            print(result)
            contentsobj = models.WebContent.objects.filter(contenttype__id__gt=2).order_by("-id")[result[0]:result[1]]
        else:
            all_count = models.WebContent.objects.filter(contenttype__id=path[2]).count()
            result = page_helper.pagerange(all_count, page,)
            contentsobj = models.WebContent.objects.filter(contenttype__id=path[2]).order_by("-id")[result[0]:result[1]]
        
        all_page = result[2]
        page_list = page_helper.pagelist_type(type_id,page, all_page)
        
        content = mark_safe(contentsobj[0].content)
        print(contentsobj[0].content)
        ret["data"] = contentsobj
        ret["content"] = content
        ret["user"] = contentsobj[0].user
        ret["page_list"] = page_list
    except Exception as e:
        ret["message"] = e
        print(e)
    
    return render_to_response("index.html",ret)



#ajax 操作-----------------------------------------------

@checklogin
def addfavor(request):
    
    ret = {"status":0,"message":'',"count":""}
    if request.method == "POST":
        try:
                      
            content_id = request.POST.get("id")
            contentobj = models.WebContent.objects.get(id=content_id)
            favor_for_id = "favor_for_webcontent"+content_id
            
            if not request.session.get(favor_for_id):
                count = contentobj.favor_count + 1
                contentobj.favor_count = count
                contentobj.save()
                ret["status"] = 1
                ret["count"] = count
            else:
                ret["message"] = "你已经点过赞了。"
                
            request.session[favor_for_id]=True
        except Exception as e:
            print(e)
            ret["message"] = "点赞失败"
    return HttpResponse(json.dumps(ret))


@checklogin
def addfavor__(request):
    
    ret = {"status":0,"message":'',"count":""}
    if request.method == "POST":
        try:
                      
            content_id = request.POST.get("id")
            contentobj = models.Comment.objects.get(id=content_id)
            favor_for_id = "favor_for_comment"+str(content_id)
            
            if not request.session.get(favor_for_id):
                count = contentobj.comment_favor + 1
                contentobj.comment_favor = count
                contentobj.save()
                ret["status"] = 1
                ret["count"] = count
            else:
                ret["message"] = "你已经点过赞了。"
                
            request.session[favor_for_id]=True
        except Exception as e:
            print(e)
            ret["message"] = "点赞失败"
    return HttpResponse(json.dumps(ret))

@checklogin
def comment(request):
    if request.method == "POST":
        try:
            content_id = request.POST.get("content_id")
            comment_content = request.POST.get("comment_content")
            #print(comment_content)
            user = models.UserInfo.objects.get(id=request.session["current_user_id"])
            #print(content_id)
            webcontent = models.WebContent.objects.get(id=content_id)
            models.Comment.objects.create(comment_user=user,
                                          comment_content=comment_content,
                                          comment_for=webcontent,
                                          )

            webcontent.comment_count += 1
            webcontent.save()
            
        except Exception as e:
            print(e)
        path = "/getarticle/"+str(content_id)
    return redirect(path)
            
def getarticle(request):
    path =  request.get_full_path()
    ret = {"content":"","comment":"","status":"","message":""}
    try:
        content_id = path.split('/')[2]
        #if content_id == 0:
        contentobj = models.WebContent.objects.get(id=content_id)
        commentobj = models.Comment.objects.filter(comment_for__id=content_id)
        ret["content"] = contentobj
        ret["comment"] = commentobj
        ret["status"] = 1
        #print(contentobj.content)
        article = mark_safe(contentobj.content)
        #print(article)
        ret["article"] = article
    except Exception as e:
        print(e)
        ret["message"] = "获取页面失败"

    return render_to_response("article.html",ret)




@checklogin
def write(request):
    ret = {"message":""}
    if request.method == "POST": 
        if request.session["current_user_id"] == 1:
            try: 
                title = request.POST.get("title")
                content_auth = request.POST.get("content_auth")
                print(title,content_auth)
                content = request.POST.get("content")
                print(content)
                content_list = []
                pattern = re.compile(r"<pre id='code'>[\s\S]*?</pre>")
                code_list = pattern.findall(content)
                print(code_list)
                content,num = pattern.subn('code',content)
                list(content)
                print(content)
                for i in content.split("\n"):
                    i ="<p>"+i+"</p>"
                    content_list.append(i)
                print(content_list)
                n =0
                for i in range(len(content_list)):
                    if content_list[i]== "<p>code</p>" or content_list[i]== "<p>code\r</p>":
                        print(content_list[i])
                        content_list[i] = code_list[n] 
                        n += 1
               
                content = mark_safe(''.join(content_list))
                print(content)
                contenttype_id = request.POST.get("contenttype")
                print(contenttype_id)
                user = models.UserInfo.objects.get(id=request.session["current_user_id"])
    
                models.WebContent.objects.create(user=user,content=content,
                                                 title=title,content_auth=content_auth,
                                                 contenttype=models.ContentType.objects.get(id=contenttype_id),)
                ret["message"] = "上传OK"
            except Exception as e:
                print(e)
                ret["message"] = "上传失败"
        else:
            return HttpResponse("权限不足")
    return render_to_response("write.html",ret)


@checklogin
def contact_content(request):
    if request.method == "POST":
        try:
            contact_content = request.POST.get("contact_content")
            user = models.UserInfo.objects.get(id=request.session["current_user_id"])
            models.Contact.objects.create(contact_user=user,
                                          contact_content=contact_content,
                                          )
            
        except Exception as e:
            print(e)
    return redirect("/contact/")
        
                                                               
                                                                         
def contact(request,page):
    ret = {"status":0,"message":'',"data":'',"page_list":''}
    try:
        page = page_helper.checkint(page)
        all_count = models.Contact.objects.all().count()
        result = page_helper.pagerange(all_count, page,)
        all_page = result[2]
        page_list = page_helper.pagelist(page, all_page)
        contents = models.Contact.objects.all().order_by("-id")[result[0]:result[1]]
        user = models.UserInfo.objects.get(id=request.session["current_user_id"])
        ret["data"] = contents
        ret["status"] = 1
        ret["page_list"] = page_list
        ret["user"] = user
    except Exception as e:
        ret["message"] = e
        print(e)
    
    return render_to_response("contact.html",ret)
choice = [1,0]
@checklogin
def addfavor_(request):
    
    ret = {"status":0,"message":'',"count":""}
    if request.method == "POST":
        try:
                      
            content_id = request.POST.get("id")
            contentobj = models.Contact.objects.get(id=content_id)
            favor_for_id = "favor_for_content"+content_id
            
            if not request.session.get(favor_for_id):
                count = contentobj.contact_favor + 1
                contentobj.contact_favor = count
                contentobj.save()
                ret["status"] = 1
                ret["count"] = count
            else:
                ret["message"] = "你已经点过赞了。"
                
            request.session[favor_for_id]=True
        except Exception as e:
            print(e)
            ret["message"] = "点赞失败"
    return HttpResponse(json.dumps(ret))


    
def about(request):

    return render_to_response("about.html")       
    
    
    
    
'''
#django自带分页-----------------------------
def index(request):
    
    contents = models.WebContent.objects.all()
    paginator = Paginator(contents,6)
    page = request.GET.get("page")
    try:
        contents = paginator.page(page)
    except PageNotAnInteger:
        contents = paginator.page(1)
    except EmptyPage:
        contents = paginator.page(paginator.num_pages)

    return render(request,"index.html",{"contents":contents})
<div class="pagination">
    <span class="step-links">
        {% if contacts.has_previous %}
            <a href="?page={{ contacts.previous_page_number }}">previous</a>
        {% endif %}
 
        <span class="current">
            Page {{ contacts.number }} of {{ contacts.paginator.num_pages }}.
        </span>
 
        {% if contacts.has_next %}
            <a href="?page={{ contacts.next_page_number }}">next</a>
        {% endif %}
    </span>
</div>
#-------------------------------------------------
'''  

        