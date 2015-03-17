from django.conf.urls import patterns, include, url
from django.contrib import admin
from authors import views

urlpatterns = patterns('',
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^author/(?P<username>\w+)/$', views.author, name='author'),
    url(r'^manage/$', views.author_manage, name='author_manage'),
    url(r'^friend_request/$', views.friend_request, name='friend_request'),
    url(r'^add_friend/$', views.add_friend, name='add_friend'),
    url(r'^remove_friend/$', views.remove_friend, name='remove_friend'),
    url(r'^$', views.index, name='index')
)
