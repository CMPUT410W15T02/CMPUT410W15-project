from django.conf.urls import patterns, include, url
from django.contrib import admin
from authors import views
from django.conf import settings

urlpatterns = patterns('',
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^accounts/login/$', views.user_login),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^author/(?P<userid>.+)/$', views.author, name='author'),
    url(r'^manage/$', views.author_manage, name='author_manage'),
    url(r'^friend_request/$', views.friend_request, name='friend_request'),
    url(r'^add_friend/$', views.add_friend, name='add_friend'),
    url(r'^remove_friend/$', views.remove_friend, name='remove_friend'),
    url(r'^manage/(?P<path>.*)$', 'django.views.static.serve', {
    'document_root': settings.MEDIA_ROOT}),
    url(r'^follow_author/$', views.follow_author, name='follow_author'),
    url(r'^unfollow_author/$', views.unfollow_author, name='unfollow_author'),
    url(r'^$', views.index, name='index'),
    url(r'^post_template/$', views.ajax_retrieve_latest_post, name='post_template')
)
