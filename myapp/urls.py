from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views

from .views import *

urlpatterns = [
    url(r'^$', views.login),
    url(r'^create_root/$', create_root),
    url(r'^create_node/$', create_node),
    url(r'^insrow/$', insrow),
    url(r'^show_trees/$', show_trees),
    url(r'^show_node/$', show_node),
    url(r'^save_node/$', save_node),
    url(r'^tree_details/$', tree_details),
    url(r'^delete_node/$', delete_node),
    url(r'^save_table/$', save_table),
    url(r'^logout/$', logout_page),
]
