from django.conf.urls import patterns, include, url
from django.contrib import admin
from posts import views

urlpatterns = patterns('',
    url(r'^posts/$', views.posts, name='posts'),
)