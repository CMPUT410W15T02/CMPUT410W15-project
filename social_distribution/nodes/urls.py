from django.conf.urls import patterns, include, url
from django.contrib import admin
from nodes import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'social_distribution.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'test/$', views.test, name='test'),
    )
