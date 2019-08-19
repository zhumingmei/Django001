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
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from app01 import views

urlpatterns = [

    ###################删除出版社，书籍和作者整合###################
    url(r'^del_(author|publisher|book)/(\d+)/', views.delete),

    ###################出版社管理系统############################
    url(r'^publisher_system/', views.publisher_system, name='publisher'),
    url(r'^add_publisher/', views.add_publisher),
    # url(r'^del_publisher/(\d+)/', views.del_publisher),
    url(r'^edit_publisher/(\d+)/', views.edit_publisher),

    ##################图书管理系统##########################
    url(r'^book_system/', views.book_system, name='book'),
    # url(r'^add_book/', views.add_book),
    url(r'^add_book/', views.AddBook.as_view()),
    # url(r'^del_book/(\d+)/', views.del_book),

    # id通过分组命名之后，作为参数传递
    # url(r'^edit_book/', views.edit_book),
    url(r'^edit_book/(\d+)/', views.edit_book),

    #################作者管理系统#########################
    url(r'^author_system/', views.author_system, name='author'),
    url(r'^add_author/', views.add_author),
    # url(r'^del_author/(\d+)/', views.del_author),
    url(r'^edit_author/(?P<pk>\d+)/', views.edit_author),

    ######################动态路由test#############################
    # 静态路由
    url(r'^index/$', views.index),

    # 动态路由
    url(r'^index/[0-9]{3}/$', views.indexs),
    url(r'^index/[0-9]{3}$|dex[123]{2}$', views.index),  # http://127.0.0.1:8068/dex23

    # 分组命名匹配
    # 分组之后，会按照位置参数进行传参,参数个数无限制
    # 传一个参数
    url(r'^index/([0-9]{3})/$', views.years),

    # 传两个参数，只要是分组，就当作是一个参数传递
    url(r'^index/([a-z]{4})/(\d{4})/$', views.yearsmonth),

    # 分组命名之后，将捕获的参数，会按照关键字参数进行传参,参数个数无限制
    # 用分组或者命名分组看情况而定，推荐使用命名分组，名字和参数名要一样，因为是关键字参数
    # 捕获的参数都是字符串形式，路径+参数，最后匹配的还是路径
    url(r'^index/(?P<yy>[a-z]{3})/(?P<mm>\d{3})/$', views.year),

    # 再形参位置给num传递了一个默认值，这样不传递参数就用num默认值
    # 如果传入新的num值将覆盖掉num默认值，使用最新的num值
    url(r'^index2/$', views.index2),

    # http://127.0.0.1:8068/index2/page236/
    url(r'^index2/page(?P<num>[0-9]{3})/$', views.index2),  

    ######################路由分发器#######################
    # 例如我访问的路径是：http://127.0.0.1:8068/app01/blog/666/
    # 先将app01 和 url路径中的app01进行匹配，剩余的/blog/666/在app01下的路径相匹配
    # app01/ 中的/不能不加，必须加上斜杠 app01和后面的路径要拼接所以要加

    url(r'^app01/', include('app01.urls',namespace='app01')),
    url(r'^app02/', include('app02.urls',namespace='app02')),

]
