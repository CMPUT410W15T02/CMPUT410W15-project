from django.conf.urls import patterns, include, url
from django.contrib import admin
from posts import views, api

urlpatterns = patterns('',
    url(r'^posts/$', views.posts, name='posts'),
    url(r'^author/(?P<author_id>.+)/posts/$', views.posts_by_author, name='author/author_id/posts'),
    url(r'^posts/all/$', views.public_posts, name='posts/all'),
    url(r'^delete/post/(?P<post_id>.+)$', views.delete_post, name='delete/post/post_id'),
    url(r'^edit/post/(?P<post_id>.+)$', views.edit_post, name='edit/post/post_id'),
    url(r'^api/author/posts/$', api.author_posts, name="api/author/posts"),
    url(r'^api/posts/$', api.posts, name="api/posts"),
    url(r'^api/author/(?P<author_id>.+)/posts/$', api.authorid_posts, name="api/author/author_id/posts"),
    url(r'^api/posts/(?P<post_id>.+)/$', api.postid_post, name="api/posts/post_id"),
    url(r'^api/friends/(?P<friend1>.+)/(?P<friend2>.+)/$', api.friends_get, name="api/friends_get"),
    url(r'^api/friends/(?P<uuid>.+)/$', api.friends_post, name="api/friends_post"),
    url(r'^api/friendrequest/$', api.friend_request, name="api/friendrequest")
)
