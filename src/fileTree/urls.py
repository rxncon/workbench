from django.conf.urls import url
from . import views


urlpatterns = [
	#url(r'^$', views.file_list, name='list'),
    url(r'^upload/$', views.file_upload, name ='upload'),
    url(r'^upload/(?P<slug>[\w-]+)/$', views.file_upload, name ='upload'),
    url(r'^(?P<slug>[\w-]+)/$', views.file_detail, name='detail'),
    url(r'^delete/(?P<pk>\d+)/$', views.file_delete, name="delete"),
    url(r'^delete/(?P<slug>[\w-]+)/$', views.file_delete_project, name="delete_project"),
]