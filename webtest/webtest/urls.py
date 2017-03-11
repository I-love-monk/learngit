"""webtest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from web import  views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^register/', views.register),
    #url(r'^captcha/$', views.captcha),
    url(r'^index/(\d*)', views.index),
    url(r'^index_type/(?P<type_id>\d*)/(?P<page>\d*)', views.index_type),
    url(r'^addfavor/', views.addfavor),
    url(r'^addfavor_/', views.addfavor_),
    url(r'^addfavor__/', views.addfavor__),
    url(r'^getarticle/', views.getarticle),
    url(r'^comment/', views.comment),
    url(r'^write/', views.write),
    url(r'^contact/(?P<page>\d*)', views.contact),
    url(r'^contact_content/', views.contact_content),
    url(r'^about/', views.about),
    url(r'^activate/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$',views.active_user)
    
]
