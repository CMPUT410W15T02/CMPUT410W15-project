from django.shortcuts import render_to_response, render, redirect
from authors.forms import UserForm, UserProfileForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from authors.models import Profile, Follow
from posts.models import Post
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
import urllib, urllib2
import json
import markdown2

# Create your views here.
def index(request):
    list_of_users = User.objects.filter( Q(username=request.user) | Q(username='admin'))
    list_of_profiles = Profile.objects.exclude(id__in=list_of_users)
    list_of_posts = []
    list_of_github = []
    # for post in post_query:
    #     if post.author == profile:
    #         list_of_posts.append(post)

    if request.user.is_authenticated():
        my_profile = Profile.objects.get(user=request.user)

        if my_profile.github != '':
            github_url = 'https://api.github.com/users/' + my_profile.github + '/received_events'

            response = urllib2.urlopen(github_url).read()
            data = json.loads(response)
            for event in data:
                if event['type'] == 'PushEvent':
                    github_post = Post(title='Push: ' + event['actor']['login'],
                    description=event['repo']['name'], privacy='2',
                    post_text=event['payload']['commits'][0]['message'], author=my_profile,
                    date=event['created_at'])
                    list_of_github.append(github_post)

                elif event['type'] == 'IssuesEvent':
                    github_post = Post(title='Issue: ' + event['actor']['login'],
                    description=event['payload']['action'], privacy='2',
                    post_text=event['payload']['issue']['title'], author=my_profile,
                    date=event['created_at'])
                    list_of_github.append(github_post)

                elif event['type'] == 'GollumEvent':
                    github_post = Post(title='Wiki: ' + event['actor']['login'],
                    description=event['repo']['name'], privacy='2',
                    post_text=event['payload']['pages'][0]['title'], author=my_profile,
                    date=event['created_at'])
                    list_of_github.append(github_post)

                elif event['type'] == 'CreateEvent':
                    github_post = Post(title='Create: ' + event['actor']['login'],
                    description=event['repo']['name'], privacy='2',
                    post_text=event['payload']['ref'], author=my_profile,
                    date=event['created_at'])
                    list_of_github.append(github_post)

                elif event['type'] == 'DeleteEvent':
                    github_post = Post(title='Delete: ' + event['actor']['login'],
                    description=event['repo']['name'], privacy='2',
                    post_text=event['payload']['ref'], author=my_profile,
                    date=event['created_at'])
                    list_of_github.append(github_post)

                else:
                    print(event)
    else:
        my_profile = ''

    if request.user.is_authenticated():
        context = RequestContext(request)
        profile = Profile.objects.get(user_id = request.user.id)
        post_query = Post.objects.filter(Q(privacy=1) | Q(privacy=3) | Q(privacy=4) | Q(author=profile)).order_by('-date')

        for post in post_query:
            if (post.content_type == 'text/x-markdown'):
                post.post_text = markdown2.markdown(post.post_text)

            if (post.privacy == '1'):
                if post.author == profile:
                    list_of_posts.append(post)
                    continue

                friends_list = profile.friends.all()
                for friend in friends_list:
                    if post.author == friend:
                        list_of_posts.append(post)
            elif ((post.privacy == '3') or (post.privacy == '4')):
                allowed_users = post.allowed.all()
                for user in allowed_users:
                    if user.id == request.user.id:
                        list_of_posts.append(post)
            elif (post.author == profile):
                list_of_posts.append(post)

    return render(request, 'authors/index.html', {'list_of_profiles':list_of_profiles, 'list_of_posts':list_of_posts, 'list_of_github':list_of_github, 'my_profile':my_profile})


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
            profile.host = request.get_host()
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
        "<a href=/author/"+request.user.username+">here</a> to return to your profile.")
    else:
        return render_to_response('authors/manage.html',
            {'profile_form': profile_form}, context)

#Send Friend Request
def friend_request(request):
    if request.method == 'POST':
        to_profile_id = request.POST.get('to_profile','')
        current_profile = Profile.objects.get(user_id=request.user.id)
        to_profile = Profile.objects.get(id=to_profile_id)

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

        if 'accept' in request.POST:
            current_profile.friends.add(from_profile)
            current_profile.save()

            #Remove from follow
            qs = Follow.objects.filter(from_profile_id=from_profile.id).filter(to_profile_id=current_profile.id)
            qs.delete()

            #Add new friend to all friend's post
            posts_qs = Post.objects.filter( Q(privacy=4) & Q(author=from_profile.id))

            for post in posts_qs:
                post.allowed.add(User.objects.get(id=current_profile.user_id))

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
