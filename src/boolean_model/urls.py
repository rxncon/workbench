from django.conf.urls import url
from . import views
from .views import Bool


urlpatterns = [
    url(r'^bool/$', views.bool, name='regGraph'),
    url(r'^bool/(?P<system_id>\d+)/$', Bool.as_view(), name='reaGraphCreate'),
    url(r'^delete/(?P<pk>\d+)/$', views.bool_delete, name="delete"),

]