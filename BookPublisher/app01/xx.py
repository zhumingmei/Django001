from django.conf.urls import url
from . import views
urlpatterns = [
    #####命名空间#########
    url(r'^index/$', views.index, name='index'),
]