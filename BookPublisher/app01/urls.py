"""BookPublisher URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/',d include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from app01 import views

urlpatterns = [
    # 反向解析
    url(r'^index/$', views.index,name='index'),
    url(r'^index3/$', views.index3,y = 123),

    # 因为我定义了name，所以无论我的路径怎么修改，前端都能通过name去找到对应的处理函数
    # 静态路由
    url(r'^blog999995588kkk/$', views.blog, name='blog'),

    # 动态路由
    url(r'^blogs/([0-9]{3})/$', views.blogs, name='blogs'),

    # 分组命名匹配
    # 分组之后，会按照位置参数进行传参,参数个数无限制
    # 传一个参数
    # http://127.0.0.1:8068/app01/blog/666/
    url(r'^blog/([0-9]{3})/$', views.blog),

    # 传两个参数，只要是分组，就当作是一个参数传递
    # http://127.0.0.1:8068/app01/blog/abcd/8888/
    url(r'^blog/(?P<years>[a-z]{4})/(?P<months>\d{4})/$', views.blog2, name='blog2'),

    #####命名空间#########
    url(r'^home/$', views.home, name='home'),

    #特殊情况，先了解，app01下又包含了一个分发器
    # url(r'^xxxx/', include('app01.xx',namespace='xx')),

]
