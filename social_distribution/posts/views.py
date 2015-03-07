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

# create new posts 
def posts(request):
    
    context = RequestContext(request)
    
    # retrieve form data
    if request.method == 'POST':
        post_form = PostForm(request.user,data=request.POST)
        if post_form.is_valid():
            privacy = post_form.cleaned_data['privacy']
            post_text = post_form.cleaned_data['post_text']
            title = post_form.cleaned_data['title']
            date = datetime.now()
            
            # get current user
            currentUser=request.user
            
            # if profile for current user already exists, retrieve it
            try:
                author=Profile.objects.get(user=currentUser)
                
            # create new profile for current user if one doesn't exist
            except:
                userObject = User.objects.get(username=currentUser)
                profile = Profile.create_profile(userObject)
                profile.host = request.get_host()
                profile.save()
                author = profile
            
            # create a new post given the form submission data                
            newPost = Post(post_text=post_text, title=title, date=date,author=author,privacy=privacy)
            
            # save the new post in the database
            newPost.save()
            
            # special privacy settings: custom	    
            if privacy=="3":
                allowed=post_form.cleaned_data['allowed']
                for user in allowed: 
                    newPost.allowed.add(User.objects.get(username=user))
                newPost.allowed.add(User.objects.get(username=author))
            
            # special privacy settings: friends	
            elif privacy=="4":
                all_friends=Profile.objects.get(user=currentUser)
                for friend in all_friends.friends.all():
                    newPost.allowed.add(User.objects.get(username=friend.user))
                newPost.allowed.add(User.objects.get(username=author))
            
            # special privacy settings: private
            elif privacy=="2":
                newPost.allowed.add(User.objects.get(username=author))
            
            # no privacy set, display error
            else:
                print post_form.errors  
            
            # once the new post is added, return to homepage
            return redirect('/')
    
    # display the post form            
    else:
        post_form = PostForm(request.user)
        
    return render(request, 'posts/posts.html', {'post_form':post_form})
    