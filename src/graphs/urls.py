from django.conf.urls import url
from . import views


urlpatterns = [
	#url(r'^$', views.file_list, name='list'),
    url(r'^regGraph/$', views.regGraph, name='regGraph'),
    url(r'^regGraph/(?P<file_id>\d+)/$', views.regGraph, name ='regGraphCreate'),
    # url(r'^upload/(?P<slug>[\w-]+)/$', views.file_upload, name ='upload'),
    url(r'^delete/(?P<pk>\d+)/$', views.graph_delete, name="delete"),
    # url(r'^delete/(?P<slug>[\w-]+)/$', views.file_delete_project, name="delete_project"),
    # url(r'^load/(?P<id>\d+)/$', views.file_load, name="load"),

]