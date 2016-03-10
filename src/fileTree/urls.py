from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^$', views.file_list, name='list'),
    #url(r'^create/$', views.post_create),
    #url(r'^(?P<slug>[\w-]+)/$', views.post_detail, name='detail'),
]