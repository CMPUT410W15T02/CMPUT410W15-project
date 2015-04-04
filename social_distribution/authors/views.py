from django.shortcuts import render_to_response, render, redirect
from authors.forms import UserForm, UserProfileForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from authors.models import Profile, Follow
from posts.models import Post
from nodes.models import Host
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
import urllib, urllib2
import json
import markdown2
from urlparse import urlparse
from operator import attrgetter
# Create your views here.
@login_required
def index(request):
    list_of_users = User.objects.filter( Q(username=request.user) | Q(username='admin'))
    list_of_profiles = Profile.objects.exclude(id__in=list_of_users)
    list_of_posts = []
    list_of_github = []

        #Checks status of friend requests sent to remote servers
    if request.user.is_authenticated():
        current_profile = Profile.objects.get(user_id = request.user.id)
        follow_qs = Follow.objects.filter(from_profile_id=current_profile.id).filter(status='PENDING')
 
        for follow in follow_qs:
            #check each follow to_profile to see if they are remote or local
            to_profile_host = follow.to_profile_id.host
 
            host_port = to_profile_host.strip("http://").split(":")
 
            port = host_port[1]
 
            if str(port) != "8000" and str(port) != "41024":
            #if str(port) == '8000' or str(port) == '41024':
                print("not local -- friend response")
                host = Host.objects.filter( Q(host_url__icontains=port) ).first()
                #host = Host.objects.filter( Q(host_url__icontains='41024') ).first()
                friend_response = host.get_friend_response(str(current_profile.uuid), str(follow.to_profile_id.uuid))
                print(friend_response['friends'])
                if friend_response['friends'].upper() == "YES" or friend_response['friends'] == True:
                    current_profile.friends.add(follow.to_profile_id)
                    current_profile.save()
                    follow.delete()

    if request.user.is_authenticated():
        my_profile = Profile.objects.get(user=request.user)

        if my_profile.github != '':
            '''try:
                github_url = 'https://api.github.com/users/' + my_profile.github + '/received_events'

                response = urllib2.urlopen(github_url).read()
                data = json.loads(response)
                for event in data:
                    if event['type'] == 'PushEvent':
                        github_post = Post(title=event['actor']['login']+' pushed to '+event['repo']['name'],
                        privacy='2', post_text=event['payload']['commits'][0]['message'],
                        author=my_profile, date=event['created_at'])
                        list_of_github.append(github_post)

                    elif event['type'] == 'IssuesEvent':
                        github_post = Post(title=event['actor']['login']+' '+event['payload']['action']+
                        ' issue at <a href='+event['payload']['issue']['html_url']+'>'+event['repo']['name']+'</a>',
                        privacy='2', post_text=event['payload']['issue']['title'],
                        author=my_profile, date=event['created_at'])
                        list_of_github.append(github_post)

                    elif event['type'] == 'GollumEvent':
                        wiki_count = 0
                        for wiki_page in event['payload']['pages']:
                            github_post = Post(title=event['actor']['login']+' '+
                            event['payload']['pages'][wiki_count]['action']+' the '+
                            event['repo']['name']+' wiki',
                            privacy='2', post_text=event['payload']['pages'][wiki_count]['action']+' '+
                            event['payload']['pages'][wiki_count]['title'],
                            author=my_profile, date=event['created_at'])
                            wiki_count += 1
                            list_of_github.append(github_post)

                    # elif event['type'] == 'CreateEvent':
                    #     github_post = Post(title='Create: ' + event['actor']['login'],
                    #     description=event['repo']['name'], privacy='2',
                    #     post_text=event['payload']['ref'], author=my_profile,
                    #     date=event['created_at'])
                    #     list_of_github.append(github_post)

                    # elif event['type'] == 'DeleteEvent':
                    #     github_post = Post(title='Delete: ' + event['actor']['login'],
                    #     description=event['repo']['name'], privacy='2',
                    #     post_text=event['payload']['ref'], author=my_profile,
                    #     date=event['created_at'])
                    #     list_of_github.append(github_post)

                    else:
                        pass
            except:
                pass'''
    else:
        my_profile = ''

    if request.user.is_authenticated():
        profile = Profile.objects.get(user_id = request.user.id)
        post_query = Post.objects.filter(Q(privacy=1) | Q(privacy=3) | Q(privacy=4) | Q(author=profile)).order_by('-date')
        post_query = list(post_query)

        hosts = Host.objects.all().exclude( Q(name='Our own') | Q(name='Test'))
        for host in hosts:
            try:
                host_posts = host.get_public_posts()
                for post in host_posts:
                    author = post['post_author']

                    #Create new remote user
                    try:
                        new_user = User.objects.get(username=author['author_details']['username'])
                    except User.DoesNotExist:
                        new_user = User(username=author['author_details']['username'], password='')
                        new_user.save()

                    #Create new remote profile
                    try:
                        new_profile = Profile.objects.get(user=new_user)
                    except Profile.DoesNotExist:
                        new_profile = Profile(host=host.host_url, uuid=author['user'], displayname="Testing", user=new_user)
                        new_profile.save()

                    #Get remote posts
                    title = post['post_title']
                    uuid = post['post_id']
                    description = post['description']
                    content_type = post['content-type']
                    content_type = "text/plain"
                    post_text = post['post_text']
                    #date = datetime.strptime(post['pubDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    date = timezone.now()

                    new_post = Post(uuid=uuid, title=title, description="", author=new_profile, date=date,content_type=content_type,post_text=post_text,privacy=1)
                    post_query.append(new_post)
            except:
                pass


        post_query.sort(key=lambda x: x.date,reverse=True)

        following_profiles = Follow.objects.filter(from_profile_id=profile.id)
        friends_list = profile.friends.all()

        for post in post_query:
            if (post.content_type == 'text/x-markdown'):
                post.post_text = markdown2.markdown(post.post_text)

            if (post.privacy == '1'):
                # Get posts from local friends
                # Friends means follow. So we also have to get the public posts of all friends
                for friend in friends_list:
                    if post.author == friend:
                        list_of_posts.append(post)

                # Get posts from the people the current user follows.
                for follow in following_profiles:
                    if post.author == follow.to_profile_id:
                        list_of_posts.append(post)

            elif ((post.privacy == '3') or (post.privacy == '4')):
                allowed_users = post.allowed.all()
                for user in allowed_users:
                    if user.id == request.user.id:
                        list_of_posts.append(post)
            # Displays your own posts
            elif (post.author == profile):
                list_of_posts.append(post)

    return render(request, 'authors/index.html',
        {'list_of_profiles':list_of_profiles, 'list_of_posts':list_of_posts, 'list_of_github':list_of_github, 'my_profile':my_profile})


def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.is_active = False
            user.save()

            profile = Profile.create_profile(user)
            profile.host = "http://cs410.cs.ualberta.ca:41024"
            profile.save()

            registered = True

        else:
            print user_form.errors

    else:
        user_form = UserForm()

    if registered == True:
        return HttpResponse("User successfully created! Login "
        "<a href=/login/>here</a> after the admin has activated your account.")
    else:
        return render_to_response('authors/register.html',
            {'user_form': user_form, 'registered': registered}, context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("This user has not been enabled by the admin yet.<br/><a href=\"/login/\">Login</a>")
        else:
            print("Invalid login deatils: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.<br/><a href=\"/login/\">Login</a>")
    else:
        return render(request, 'authors/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

def author(request, userid):
    if request.user.is_authenticated():
        current_profile = Profile.objects.get(user_id=request.user.id)
    else:
        current_profile = ''

    profile = Profile.objects.get(uuid = userid)
    user = profile.user

    #Check if friends and following
    isFriends = False
    isFollowing = False
    sentFR = False

    if request.user.is_authenticated():
        friend_qs = current_profile.friends.filter(id=profile.id)
        follow_qs = Follow.objects.filter( Q(from_profile_id=current_profile) & Q(to_profile_id=profile) ).first()

        if(friend_qs):
            isFriends = True

        if(follow_qs):
            isFollowing = True
            if(follow_qs.status ==  "PENDING"):
                sentFR = True

    return render(request, 'authors/author.html',
        {'profile':profile, 'user_object':user,'isFriends':isFriends, 'isFollowing':isFollowing, "sentFR":sentFR, 'current':request.user, 'my_profile':current_profile})

@login_required
def author_manage(request):
    context = RequestContext(request)
    profile = Profile.objects.get(user_id=request.user.id)
    updated = False

    if request.user.is_authenticated():
        my_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST)

        if profile_form.is_valid():
            profile.displayname = profile_form.cleaned_data['displayname']
            profile.body = profile_form.cleaned_data['body']
            profile.birthdate = profile_form.cleaned_data['birthdate']
            profile.gender = profile_form.cleaned_data['gender']
            newclear = request.POST.get('image-clear')
            print(newclear)
            #profile.image = profile_form.cleaned_data['image']
            try:
                profile.image = request.FILES['image']
            except:
                if newclear == "on":
                    profile.image=""

            profile.github = profile_form.cleaned_data['github']
            profile.workspace = profile_form.cleaned_data['workspace']
            profile.school = profile_form.cleaned_data['school']
            profile.save()

            updated = True
        else:
            print profile_form.errors

    else:
        profile_form = UserProfileForm(instance=profile)

    if updated == True:
        return HttpResponse("Profile Successfully edited! Click "
        "<a href=/author/"+my_profile.uuid+">here</a> to return to your profile.")
    else:
        return render_to_response('authors/manage.html',
            {'profile_form': profile_form, 'my_profile':my_profile}, context)

#Send Friend Request
def friend_request(request):
    if request.method == 'POST':
        to_profile_id = request.POST.get('to_profile','')
        current_profile = Profile.objects.get(user_id=request.user.id)
        to_profile = Profile.objects.get(id=to_profile_id)

        host_port = to_profile.host.strip("http://").split(":")
        print(host_port)
        port = host_port[1]

        if str(port) != "8000" and str(port) != "41024":
            print("Not Local")
            #host = Host.objects.get(name="Our own")
            host = Host.objects.filter( Q(host_url__icontains=port) ).first()
            host.post_friend_request([str(current_profile.uuid), str(to_profile.uuid)])
            #print(host)

        checkFollow = Follow.objects.filter( Q(from_profile_id=current_profile) & Q(to_profile_id=to_profile) ).first()
        if checkFollow:
            checkFollow.status ="PENDING"
            checkFollow.save()
        else:
            newFollow = Follow(from_profile_id=current_profile, to_profile_id=to_profile, status='PENDING')
            newFollow.save()

    return redirect('/')

#Accept or Reject Friend Reject
@login_required
def add_friend(request):
    current_profile = Profile.objects.get(user_id=request.user.id)
    friends = None

    if request.method == 'POST':
        from_profile_id = request.POST.get('from_profile', '')
        from_profile = Profile.objects.get(id=from_profile_id)

        host_port = from_profile.host.strip("http://").split(":")

        port = host_port[1]

        if 'accept' in request.POST:
            current_profile.friends.add(from_profile)
            current_profile.save()

            #Remove from follow
            qs = Follow.objects.filter(from_profile_id=from_profile.id).filter(to_profile_id=current_profile.id)
            qs.delete()

            #Add new friend to all friend's post
            posts_qs = Post.objects.filter( Q(privacy=4) & Q(author=from_profile.id))

            for post in posts_qs:
                post.allowed.add(Profile.objects.get(id=current_profile.id))

        elif 'reject' in request.POST:
            #change status form PENDING to REJECT
            qs = Follow.objects.filter(from_profile_id=from_profile_id).filter(to_profile_id=current_profile.id).update(status='FOLLOWING')
        return redirect('index')
    else:
        qs = Follow.objects.filter(to_profile_id=current_profile.id).filter(status='PENDING')
        if qs:
            friends = qs
        return render(request, 'authors/add_friend.html',{'friends':friends, 'my_profile':current_profile})

#Remove friends
def remove_friend(request):
    current_profile = Profile.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        remove_profile_id = request.POST.get('remove_profile_id', '')
        remove_profile = Profile.objects.get(id=remove_profile_id)

        posts_qs = Post.objects.filter( Q(privacy=4) & Q(author=current_profile.id))

        for post in posts_qs:
            post.allowed.remove(Profile.objects.get(id=remove_profile.id))

        current_profile.friends.remove(remove_profile)

    return redirect('/')

#Follow an author
def follow_author(request):
    current_profile = Profile.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        follow_profile_id = request.POST.get("follow_profile_id"," ")
        follow_profile = Profile.objects.get(id=follow_profile_id)

        newFollow = Follow(from_profile_id=current_profile, to_profile_id=follow_profile, status='FOLLOWING')
        newFollow.save()

    return redirect('/')

#unfollow an author
def unfollow_author(request):
    current_profile = Profile.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        unfollow_profile_id = request.POST.get("unfollow_profile_id"," ")
        unfollow_profile = Profile.objects.get(id=unfollow_profile_id)

        unfollow = Follow.objects.filter(from_profile_id=current_profile).filter(to_profile_id=unfollow_profile)
        unfollow.delete()

    return redirect('/')

def ajax_retrieve_latest_post(request):
    list_of_posts = []

    if request.user.is_authenticated():
        profile = Profile.objects.get(user_id = request.user.id)
        post_query = Post.objects.filter(Q(privacy=1) | Q(privacy=3) | Q(privacy=4) | Q(author=profile)).order_by('-date')
        post_query = list(post_query)

        hosts = Host.objects.all().exclude( Q(name='Our own') | Q(name='Test'))
        for host in hosts:
            try:
                host_posts = host.get_public_posts()
                for post in host_posts:
                    author = post['post_author']

                    #Create new remote user
                    try:
                        new_user = User.objects.get(username=author['author_details']['username'])
                    except User.DoesNotExist:
                        new_user = User(username=author['author_details']['username'], password='')
                        new_user.save()

                    #Create new remote profile
                    try:
                        new_profile = Profile.objects.get(user=new_user)
                    except Profile.DoesNotExist:
                        new_profile = Profile(host=host.host_url, uuid=author['user'], displayname="Testing", user=new_user)
                        new_profile.save()

                    #Get remote posts
                    title = post['post_title']
                    uuid = post['post_id']
                    description = post['description']
                    content_type = post['content-type']
                    content_type = "text/plain"
                    post_text = post['post_text']
                    #date = datetime.strptime(post['pubDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    date = timezone.now()

                    new_post = Post(uuid=uuid, title=title, description="", author=new_profile, date=date,content_type=content_type,post_text=post_text,privacy=1)
                    post_query.append(new_post)
            except:
                pass


        post_query.sort(key=lambda x: x.date,reverse=True)

        following_profiles = Follow.objects.filter(from_profile_id=profile.id)
        friends_list = profile.friends.all()

        for post in post_query:
            if (post.content_type == 'text/x-markdown'):
                post.post_text = markdown2.markdown(post.post_text)

            if (post.privacy == '1'):
                # Get posts from local friends
                # Friends means follow. So we also have to get the public posts of all friends
                for friend in friends_list:
                    if post.author == friend:
                        list_of_posts.append(post)

                # Get posts from the people the current user follows.
                for follow in following_profiles:
                    if post.author == follow.to_profile_id:
                        list_of_posts.append(post)

            elif ((post.privacy == '3') or (post.privacy == '4')):
                allowed_users = post.allowed.all()
                for user in allowed_users:
                    if user.id == request.user.id:
                        list_of_posts.append(post)
            # Displays your own posts
            elif (post.author == profile):
                list_of_posts.append(post)
    
    return render(request, 'post_template.html', {'list_of_posts': list_of_posts})

def ajax_retrieve_latest_github(request):
    list_of_github = []

    if request.user.is_authenticated():
        my_profile = Profile.objects.get(user_id = request.user.id)

        if my_profile.github != '':
            try:
                github_url = 'https://api.github.com/users/' + my_profile.github + '/received_events'

                response = urllib2.urlopen(github_url).read()
                data = json.loads(response)
                for event in data:
                    if event['type'] == 'PushEvent':
                        github_post = Post(title=event['actor']['login']+' pushed to '+event['repo']['name'],
                        privacy='2', post_text=event['payload']['commits'][0]['message'],
                        author=my_profile, date=event['created_at'])
                        list_of_github.append(github_post)

                    elif event['type'] == 'IssuesEvent':
                        github_post = Post(title=event['actor']['login']+' '+event['payload']['action']+
                        ' issue at <a href='+event['payload']['issue']['html_url']+'>'+event['repo']['name']+'</a>',
                        privacy='2', post_text=event['payload']['issue']['title'],
                        author=my_profile, date=event['created_at'])
                        list_of_github.append(github_post)

                    elif event['type'] == 'GollumEvent':
                        wiki_count = 0
                        for wiki_page in event['payload']['pages']:
                            github_post = Post(title=event['actor']['login']+' '+
                            event['payload']['pages'][wiki_count]['action']+' the '+
                            event['repo']['name']+' wiki',
                            privacy='2', post_text=event['payload']['pages'][wiki_count]['action']+' '+
                            event['payload']['pages'][wiki_count]['title'],
                            author=my_profile, date=event['created_at'])
                            wiki_count += 1
                            list_of_github.append(github_post)

                    # elif event['type'] == 'CreateEvent':
                    #     github_post = Post(title='Create: ' + event['actor']['login'],
                    #     description=event['repo']['name'], privacy='2',
                    #     post_text=event['payload']['ref'], author=my_profile,
                    #     date=event['created_at'])
                    #     list_of_github.append(github_post)

                    # elif event['type'] == 'DeleteEvent':
                    #     github_post = Post(title='Delete: ' + event['actor']['login'],
                    #     description=event['repo']['name'], privacy='2',
                    #     post_text=event['payload']['ref'], author=my_profile,
                    #     date=event['created_at'])
                    #     list_of_github.append(github_post)

                    else:
                        pass
            except Exception as e:
                pass
    else:
        my_profile = ''

    return render(request, 'github_template.html', {'list_of_github': list_of_github, 'my_profile': my_profile})
