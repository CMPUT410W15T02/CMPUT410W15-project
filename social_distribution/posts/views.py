from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from posts.forms import PostForm
from django.http import HttpResponseRedirect, HttpResponse
from posts.models import Post
from authors.models import Profile
from datetime import datetime
from django.contrib.auth.models import User

import time
# Create your views here. 
def posts(request):
    context =RequestContext(request)
    
    if request.method == 'POST':
        post_form = PostForm(request.user,data=request.POST)
        if post_form.is_valid():
            privacy = post_form.cleaned_data['privacy']
            post_text=post_form.cleaned_data['post_text']
            title=post_form.cleaned_data['title']
	    date=datetime.now()
	    current=request.user
	    author=Profile.objects.get(user=current)
	    a=Post(post_text=post_text, title=title, date=date,author=author,privacy=privacy)
	    a.save()	    
            if privacy=="3":
		allowed=post_form.cleaned_data['allowed']
                for user in allowed: 
		    a.allowed.add(User.objects.get(username=user))
		a.allowed.add(User.objects.get(username=author))
            elif privacy=="4":
		all_friends=Profile.objects.get(user=current)
		for friend in all_friends.friends.all():
		    a.allowed.add(User.objects.get(username=friend.user))
		a.allowed.add(User.objects.get(username=author))
	    elif privacy=="2":
		a.allowed.add(User.objects.get(username=author))
        else:
            print post_form.errors  
	    
    else:
        post_form=PostForm(request.user)
    return render(request, 'posts/posts.html', {'post_form':post_form})