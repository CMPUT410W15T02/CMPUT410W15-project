from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from posts.forms import PostForm
from django.http import HttpResponseRedirect, HttpResponse
from posts.models import Post
from authors.models import Profile

import time
# Create your views here.
def posts(request):
    context =RequestContext(request)
    
    if request.method == 'POST':
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            privacy = post_form.cleaned_data['privacy']
            post_text=post_form.cleaned_data['post_text']
            title=post_form.cleaned_data['title']
            if privacy=="3":
		a=0
		#TODO When posting add all the allowed names
		#allowed=post_form.cleaned_data['allowed']
                #for user in allowed: 
		 #   allowedUsers.allowed.add(user.username)                    
            elif privacy=="4":
		a=0
		#TODO when posting get all friends names and add them to allowed names
            else:
                a=0
		#TODO when posting make allowed empty
        else:
            print post_form.errors     
    else:
        post_form=PostForm()
    return render(request, 'posts/posts.html', {'post_form':post_form})