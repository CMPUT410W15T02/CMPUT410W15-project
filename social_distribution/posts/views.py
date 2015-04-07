from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from posts.forms import PostForm, EditForm, CommentForm
from django.http import HttpResponseRedirect, HttpResponse
from posts.models import Post, Comment
from authors.models import Profile
from nodes.models import Host
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import markdown2
import time, datetime

# create new posts
@login_required
def posts(request):
    context = RequestContext(request)
    # retrieve form data
    if request.method == 'POST':
        post_form = PostForm(request.user,data=request.POST)
        if post_form.is_valid():
            privacy = post_form.cleaned_data['privacy']
            post_text = post_form.cleaned_data['post_text']
            title = post_form.cleaned_data['title']
            description = post_form.cleaned_data['description']
            content_type = post_form.cleaned_data['content_type']
            date = timezone.now()
            # check if a new photo was uploaded
            try:
                image = request.FILES['image']

            except:
                image=""

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
            newPost = Post(post_text=post_text, description=description, title=title, date=date,author=author,privacy=privacy, image=image, content_type=content_type)

            # save the new post in the database
            newPost.save()

            # special privacy settings: friend of a friend
            if privacy=="3":
                all_friends=Profile.objects.get(user=currentUser)
                for friend in all_friends.friends.all():
                    foaf=Profile.objects.get(user=User.objects.get(username=friend.user))
                    for second_friend in foaf.friends.all():
                        try:
                            newPost.allowed.add(Profile.objects.get(user=User.objects.get(username=second_friend.user)))
                        except:
                            continue
                newPost.allowed.add(Profile.objects.get(user=User.objects.get(username=author)))

            # special privacy settings: friends on this server
            elif privacy=="4":
                all_friends=Profile.objects.get(user=currentUser)
                for friend in all_friends.friends.all():
                    f=Profile.objects.get(user=User.objects.get(username=friend.user))
                    if f.host == 'http://cs410.cs.ualberta.ca:41024':
                        newPost.allowed.add(f)
                newPost.allowed.add(Profile.objects.get(user=User.objects.get(username=author)))
	     # special privacy settings: friends
	    elif privacy=="5":
                all_friends=Profile.objects.get(user=currentUser)
                for friend in all_friends.friends.all():
                    newPost.allowed.add(Profile.objects.get(user=User.objects.get(username=friend.user)))
                newPost.allowed.add(Profile.objects.get(user=User.objects.get(username=author)))

            # special privacy settings: private
            elif privacy=="2":
                newPost.allowed.add(Profile.objects.get(user=User.objects.get(username=author)))
            # once the new post is added, return to homepage
            return redirect('/')
        # display error if fields aren't filled properly
        else:
            print post_form.errors
    # display the post form
    else:
        post_form = PostForm(request.user)
    my_profile = Profile.objects.get(user=request.user)

    return render(request, 'posts/posts.html', {'post_form':post_form, 'my_profile':my_profile})

# view all posts of an author specified by author_id
@login_required
def posts_by_author(request, author_id):

    list_of_posts = []

    try:
        if request.user.is_authenticated():
            my_profile = Profile.objects.get(user=request.user)
            context = RequestContext(request)

            # get profile from author id
            #userObject = User.objects.get(username=author_id)
            profile = Profile.objects.get(uuid=author_id)
            user = profile.user

            # if the requested user is the current user show private posts too
            if(profile == request.user.profile):
                post_query = Post.objects.filter(Q(author=profile))

            # the requested user is not the current user
            else:
                post_query = Post.objects.filter(Q(author=profile) & (Q(privacy=1) | Q(privacy=3) | Q(privacy=4)) ).order_by('-date')

            for post in post_query:
                if post.content_type == 'text/x-markdown':
                    post.post_text = markdown2.markdown(post.post_text)

                # public posts by the author
                if (post.privacy == '1'):
                    if post.author == profile:
                        list_of_posts.append(post)

                # check if current user is allowed to see remaining posts
                elif ((post.privacy == '3') or (post.privacy == '4')):
                    allowed_users = post.allowed.all()
                    for user in allowed_users:
                        if user.id == request.user.id:
                            list_of_posts.append(post)

                # for when the requested user is the current user
                elif (post.author == profile):
                    list_of_posts.append(post)

        title = "Viewing Posts by " + user.username

    except:
        profile = Profile.objects.get(uuid=author_id)
        user = profile.user
        title = "There are no posts by " + user.username
    url_from = '/posts_by_author/' + author_id

    list_of_posts.sort(key=lambda x: x.date,reverse=True)

    return render(request, 'posts/view_posts.html', {'list_of_posts':list_of_posts, 'title':title, 'my_profile':my_profile, 'url_from':url_from})

# view all public posts
@login_required
def public_posts(request):
    if request.user.is_authenticated():
        my_profile = Profile.objects.get(user=request.user)
    else:
        my_profile = ''

    list_of_posts = list(Post.objects.filter(Q(privacy=1)).order_by('-date'))

    hosts = Host.objects.all()
    for host in hosts:
        try:
            host_posts = host.get_public_posts()
            if host.name == "Group3":
                for post in host_posts['posts']:
                    author = post['author']
                    #Create new remote user
                    try:
                        new_user = User.objects.get(username=author['displayname']+'@Group3')
                    except User.DoesNotExist:
                        new_user = User(username=author['displayname']+'@Group3', password='')
                        new_user.save()

                    #Create new remote profile
                    try:
                        new_profile = Profile.objects.get(user=new_user)
                    except Profile.DoesNotExist:
                        new_profile = Profile(host=author['host'], uuid=author['id'], displayname=author['displayname'], user=new_user)
                        new_profile.save()

                    #Get remote posts
                    title = post['title']
                    uuid = post['guid']
                    description = post['description']
                    content_type = post['content-type']
                    post_text = post['content']
                    date = timezone.make_aware(datetime.datetime.strptime(post['pubdate'], '%Y-%m-%d'), timezone.get_default_timezone())

                    new_post = Post(uuid=uuid, title=title, description="", author=new_profile, date=date,content_type=content_type,post_text=post_text,privacy='1')
                    list_of_posts.append(new_post)
            elif host.name == "Group7":
                for post in host_posts['posts']:
                    author = post['author']
                    #Create new remote user
                    try:
                        new_user = User.objects.get(username=author['displayname']+'@Group7')
                    except User.DoesNotExist:
                        new_user = User(username=author['displayname']+'@Group7', password='')
                        new_user.save()

                    #Create new remote profile
                    try:
                        new_profile = Profile.objects.get(user=new_user)
                    except Profile.DoesNotExist:
                        new_profile = Profile(host=author['host'], uuid=author['id'], displayname=author['displayname'], user=new_user)
                        new_profile.save()

                    #Get remote posts
                    title = post['title']
                    uuid = post['guid']
                    description = post['description']
                    content_type = post['content-type']
                    post_text = post['content']
                    #Date is set to April 1 because its not given
                    date = timezone.make_aware(datetime.datetime.strptime('2015-04-01', '%Y-%m-%d'), timezone.get_default_timezone())

                    new_post = Post(uuid=uuid, title=title, description="", author=new_profile, date=date,content_type=content_type,post_text=post_text,privacy='1')
                    list_of_posts.append(new_post)
        except:
            pass

    for post in list_of_posts:
        if post.content_type == 'text/x-markdown':
            post.post_text = markdown2.markdown(post.post_text)

    list_of_posts.sort(key=lambda x: x.date,reverse=True)

    title = "Viewing All Public Posts"
    url_from = "/public_posts/"
    return render(request, 'posts/view_posts.html', {'list_of_posts':list_of_posts, 'title':title, 'my_profile':my_profile, 'url_from':url_from})

def delete_post(request, post_id):
    Post.objects.filter(Q(uuid=post_id)).delete()
    return HttpResponse("<script>alert(\"Your post has been deleted\"); window.location = \'/\';</script>")

#Editing a post
@login_required
def edit_post(request, post_id):
    post=Post.objects.get(uuid=post_id)

    if request.user.is_authenticated():
        my_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        edit_form = EditForm(request.user, post, data=request.POST)
        if edit_form.is_valid():
            #Takes all the Posts data and overwrites it with the new data being sent
            author=Profile.objects.get(user=request.user)
            privacy = edit_form.cleaned_data['privacy']
            post_text = edit_form.cleaned_data['post_text']
            title = edit_form.cleaned_data['title']
            description = edit_form.cleaned_data['description']
            content_type = edit_form.cleaned_data['content_type']
            newclear = request.POST.get('clear')

            post.title=title
            post.post_text=post_text
            post.description=description
            post.privacy=privacy
            post.content_type=content_type

            # check if a new photo was uploaded
            try:
                image = request.FILES['image']
                post.image=image
            except:
                if (post.image == None):
                    post.image=""
                elif (newclear == "on"):
                    post.image=""
            post.save()

            post.allowed.clear()
            if privacy=="3":
		all_friends=Profile.objects.get(user=request.user)
                for friend in all_friends.friends.all():
		    foaf=Profile.objects.get(user=User.objects.get(username=friend.user))
		    for second_friend in foaf.friends.all():
			try:
                    	    post.allowed.add(Profile.objects.get(user=User.objects.get(username=second_friend.user)))
			except:
			    continue
                post.allowed.add(Profile.objects.get(user=User.objects.get(username=author)))
	    elif privacy=="4":
		all_friends=Profile.objects.get(user=request.user)
                for friend in all_friends.friends.all():
		    f=Profile.objects.get(user=User.objects.get(username=friend.user))
		    if f.host == 'http://cs410.cs.ualberta.ca:41024':
		    	post.allowed.add(f)
                post.allowed.add(Profile.objects.get(user=User.objects.get(username=author)))
            elif privacy=="5":
                all_friends=Profile.objects.get(user=request.user)
                for friend in all_friends.friends.all():
                    post.allowed.add(Profile.objects.get(user=User.objects.get(username=friend.user)))
                post.allowed.add(Profile.objects.get(user=User.objects.get(username=author)))

            # special privacy settings: private
            elif privacy=="2":
                post.allowed.add(Profile.objects.get(user=User.objects.get(username=author)))
            request.session.modified = True
            return redirect('/')
        else:
            print edit_form.errors
    else:
        edit_form = EditForm(request.user, post)

    return render(request, 'posts/posts.html', {'post_form':edit_form,'edit':'edit', 'my_profile':my_profile, 'post':post})


#view posts by friends of current logged in user
@login_required
def friends_posts(request):
    if request.user.is_authenticated():
        my_profile = Profile.objects.get(user=request.user)

    friend_qs = Post.objects.filter(Q(privacy=4) | Q(privacy=5)).exclude(allowed=None).order_by('-date') #removes posts with empty allowed list

    list_of_posts = []

    for post in friend_qs:
        if post.content_type == 'text/x-markdown':
            post.post_text = markdown2.markdown(post.post_text)
        allowed_users = post.allowed.all()
        if my_profile in allowed_users:
            list_of_posts.append(post)
    url_from = '/friends_posts/'

    list_of_posts.sort(key=lambda x: x.date,reverse=True)

    return render(request, 'posts/view_posts.html', {'list_of_posts':list_of_posts, 'title':"Friends' Posts", 'my_profile':my_profile, 'url_from':url_from})

#view posts from custom privacy
def custom_posts(request):
    if request.user.is_authenticated():
        my_profile = Profile.objects.get(user=request.user)

    custom_qs = Post.objects.filter(privacy=3).exclude(allowed=None).order_by('-date') #removes posts with empty allowed list

    list_of_posts = []

    for post in custom_qs:
        if post.content_type == 'text/x-markdown':
            post.post_text = markdown2.markdown(post.post_text)
        allowed_users = post.allowed.all()
        for user in allowed_users:
            if user.id == request.user.id:
                list_of_posts.append(post)

    return render(request, 'posts/view_posts.html', {'list_of_posts':list_of_posts, 'my_profile':my_profile})


def expand_post(request,post_id):
    if request.user.is_authenticated():
        my_profile = Profile.objects.get(user=request.user)
    try:
        post = Post.objects.get(uuid=post_id)
    except:
        hosts = Host.objects.all()
        for host in hosts:
            if host.name == "Group3":
                try:
                    post_json = host.get_postid(post_id)['posts'][0]
                    visibility = post_json['visibility']
                    description = post_json['description']
                    date = timezone.make_aware(datetime.datetime.strptime(post_json['pubdate'], '%Y-%m-%d'), timezone.get_default_timezone())
                    title = post_json['title']
                    content = post_json['content']
                    content_type = post_json['content-type']

                    author_id = post_json['author']['id']
                    author_host = post_json['author']['host']
                    author_displayname = post_json['author']['displayname']
                    try:
                        author_user = User(username=author_displayname+'@Group3',
                                            password="")
                        author_user.save()
                        author_profile = Profile(user=author_user,uuid=author_id,
                        displayname=author_displayname,host=author_host)
                        author_profile.save()
                    except:
                        author_profile = Profile.objects.get(uuid=author_id)

                    post = Post(title=title,post_text=content,author=author_profile,date=date,privacy='1')
                    comments = []
                    comment_form = []
                    return render(request, 'posts/expand_post.html',{'comments':comments, 'comment_form':comment_form, 'post':post, 'my_profile':my_profile})
                except:
                    pass
            elif host.name == "Group7":
                try:
                    post_json = host.get_postid(post_id)['posts'][0]
                    print(post_json)
                    #visibility = post_json['visibility']
                    description = post_json['description']
                    date = date = timezone.make_aware(datetime.datetime.strptime('2015-04-01', '%Y-%m-%d'), timezone.get_default_timezone())
                    title = post_json['title']
                    content = post_json['content']
                    content_type = post_json['content-type']

                    author_id = post_json['author']['id']
                    author_host = post_json['author']['host']
                    author_displayname = post_json['author']['displayname']
                    try:
                        author_user = User(username=author_displayname+'@Group3',
                                            password="")
                        author_user.save()
                        author_profile = Profile(user=author_user,uuid=author_id,
                        displayname=author_displayname,host=author_host)
                        author_profile.save()
                    except:
                        author_profile = Profile.objects.get(uuid=author_id)

                    post = Post(title=title,post_text=content,author=author_profile,date=date,privacy='1')
                    comments = []
                    comment_form = []
                    return render(request, 'posts/expand_post.html',{'comments':comments, 'comment_form':comment_form, 'post':post, 'my_profile':my_profile})
                except:
                    pass

    try:
        if post.content_type == 'text/x-markdown':
            post.post_text = markdown2.markdown(post.post_text)
        current_profile = Profile.objects.get(user_id=request.user.id)
        comments = None
        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)

            if comment_form.is_valid():
                body = comment_form.cleaned_data['body']
                newComment = Comment(body=body, date=timezone.now(), author=current_profile, post_id=post)
                newComment.save()
            else:
                print comment_form.errors
            return redirect('/posts/'+post_id)
        else:
            comments = Comment.objects.filter(post_id=post).order_by('date')
            comment_form = CommentForm()
        return render(request, 'posts/expand_post.html',{'comments':comments, 'comment_form':comment_form, 'post':post, 'my_profile':my_profile})
    except:
        return HttpResponse("Post not found", status=404)

@login_required
def ajax_friends_post(request):
    if request.user.is_authenticated():
        my_profile = Profile.objects.get(user=request.user)

    friend_qs = Post.objects.filter(Q(privacy=4) | Q(privacy=5)).exclude(allowed=None).order_by('-date') #removes posts with empty allowed list

    list_of_posts = []

    for post in friend_qs:
        if post.content_type == 'text/x-markdown':
            post.post_text = markdown2.markdown(post.post_text)
        allowed_users = post.allowed.all()
        if my_profile in allowed_users:
            list_of_posts.append(post)
    url_from = '/friends_posts/'

    list_of_posts.sort(key=lambda x: x.date,reverse=True)

    return render(request, 'post_template.html', {'list_of_posts':list_of_posts, 'title':"Friends' Posts", 'my_profile':my_profile})

@login_required
def ajax_public_posts(request):
    if request.user.is_authenticated():
        my_profile = Profile.objects.get(user=request.user)
    else:
        my_profile = ''

    list_of_posts = list(Post.objects.filter(Q(privacy=1)).order_by('-date'))

    hosts = Host.objects.all()
    for host in hosts:
        try:
            host_posts = host.get_public_posts()
            if host.name == "Group3":
                for post in host_posts['posts']:
                    author = post['author']
                    #Create new remote user
                    try:
                        new_user = User.objects.get(username=author['displayname']+'@Group3')
                    except User.DoesNotExist:
                        new_user = User(username=author['displayname']+'@Group3', password='')
                        new_user.save()

                    #Create new remote profile
                    try:
                        new_profile = Profile.objects.get(user=new_user)
                    except Profile.DoesNotExist:
                        new_profile = Profile(host=author['host'], uuid=author['id'], displayname=author['displayname'], user=new_user)
                        new_profile.save()

                    #Get remote posts
                    title = post['title']
                    uuid = post['guid']
                    description = post['description']
                    content_type = post['content-type']
                    post_text = post['content']
                    date = timezone.make_aware(datetime.datetime.strptime(post['pubdate'], '%Y-%m-%d'), timezone.get_default_timezone())

                    new_post = Post(uuid=uuid, title=title, description="", author=new_profile, date=date,content_type=content_type,post_text=post_text,privacy='1')
                    list_of_posts.append(new_post)
            elif host.name == "Group7":
                for post in host_posts['posts']:
                    author = post['author']
                    #Create new remote user
                    try:
                        new_user = User.objects.get(username=author['displayname']+'@Group7')
                    except User.DoesNotExist:
                        new_user = User(username=author['displayname']+'@Group7', password='')
                        new_user.save()

                    #Create new remote profile
                    try:
                        new_profile = Profile.objects.get(user=new_user)
                    except Profile.DoesNotExist:
                        new_profile = Profile(host=author['host'], uuid=author['id'], displayname=author['displayname'], user=new_user)
                        new_profile.save()

                    #Get remote posts
                    title = post['title']
                    uuid = post['guid']
                    description = post['description']
                    content_type = post['content-type']
                    post_text = post['content']
                    #Date is set to April 1 because its not given
                    date = timezone.make_aware(datetime.datetime.strptime('2015-04-01', '%Y-%m-%d'), timezone.get_default_timezone())

                    new_post = Post(uuid=uuid, title=title, description="", author=new_profile, date=date,content_type=content_type,post_text=post_text,privacy='1')
                    list_of_posts.append(new_post)
        except:
            pass

    for post in list_of_posts:
        if post.content_type == 'text/x-markdown':
            post.post_text = markdown2.markdown(post.post_text)

    list_of_posts.sort(key=lambda x: x.date,reverse=True)

    title = "Viewing All Public Posts"
    return render(request, 'post_template.html', {'list_of_posts':list_of_posts, 'title':title, 'my_profile':my_profile})

@login_required
def ajax_posts_by_author(request, author_id):

    list_of_posts = []


    try:
        if request.user.is_authenticated():
            my_profile = Profile.objects.get(user=request.user)
            context = RequestContext(request)

            # get profile from author id
            #userObject = User.objects.get(username=author_id)
            profile = Profile.objects.get(uuid=author_id)
            user = profile.user

            # if the requested user is the current user show private posts too
            if(profile == request.user.profile):
                post_query = Post.objects.filter(Q(author=profile))

            # the requested user is not the current user
            else:
                post_query = Post.objects.filter(Q(author=profile) & (Q(privacy=1) | Q(privacy=3) | Q(privacy=4)) ).order_by('-date')

            for post in post_query:
                if post.content_type == 'text/x-markdown':
                    post.post_text = markdown2.markdown(post.post_text)

                # public posts by the author
                if (post.privacy == '1'):
                    if post.author == profile:
                        list_of_posts.append(post)

                # check if current user is allowed to see remaining posts
                elif ((post.privacy == '3') or (post.privacy == '4')):
                    allowed_users = post.allowed.all()
                    for user in allowed_users:
                        if user.id == request.user.id:
                            list_of_posts.append(post)

                # for when the requested user is the current user
                elif (post.author == profile):
                    list_of_posts.append(post)

        title = "Viewing Posts by " + user.username

    except:
        profile = Profile.objects.get(uuid=author_id)
        user = profile.user
        title = "There are no posts by " + user.username

    list_of_posts.sort(key=lambda x: x.date,reverse=True)

    return render(request, 'post_template.html', {'list_of_posts':list_of_posts, 'title':title, 'my_profile':my_profile})
