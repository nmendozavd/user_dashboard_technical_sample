from django.conf.urls import url
from . import views
from models import *

urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.home),
    url(r'^dashboard/admin$', views.adminhome),
    url(r'^add$', views.processadd),
    url(r'^edit/(?P<user_id>\d+)$', views.edit_user),
    url(r'^editpass/(?P<user_id>\d+)$', views.edit_pass),
    url(r'^addfromadmin$', views.processaddadmin),
    url(r'^login$', views.processlogin),
    url(r'^users/addnew$', views.adminregister),
    url(r'^add_message/(?P<user_id>\d+)$', views.addmessage),
    url(r'^add_comment/(?P<user_id>\d+)/(?P<message_id>\d+)$', views.addcomment),
    url(r'^users/edit/(?P<user_id>\d+)$', views.adminedit),
    url(r'^users/edit$', views.edit_by_user),
    url(r'^update/(?P<user_id>\d+)$', views.user_update),
    url(r'^users/show/(?P<user_id>\d+)$', views.show),
    url(r'^users/remove/(?P<user_id>\d+)$', views.remove),
    url(r'^edit/desc/(?P<user_id>\d+$)', views.editdesc),
]