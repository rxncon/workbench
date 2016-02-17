from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    #url(r'^posts/$', views.post_home), not good for function type views
    #url(r'^$', "posts.views.post_home") # string with path for function type views
    url(r'^$',views.post_list),
    url(r'^create/$',views.post_create ),
    url(r'^detail/$',views.post_detail),
    url(r'^update/$',views.post_update ),
    url(r'^delete/$',views.post_delete ),
]