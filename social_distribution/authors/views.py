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

# Create your views here.
def index(request):
    list_of_users = User.objects.exclude( Q(username=request.user) | Q(username='admin'))
    list_of_posts = []
    # for post in post_query:
    #     if post.author == profile:
    #         list_of_posts.append(post)

    if request.user.is_authenticated():
        context = RequestContext(request)
        profile = Profile.objects.get(user_id = request.user.id)
        post_query = Post.objects.filter(Q(privacy=1) | Q(privacy=3) | Q(privacy=4) | Q(author=profile)).order_by('-date')

        for post in post_query:
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


    return render(request, 'authors/index.html', {'list_of_users':list_of_users, 'list_of_posts':list_of_posts})


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
    return HttpResponseRedirect('/')

def author(request, username):
    context = RequestContext(request)
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user_id = user.id)
    return render(request, 'authors/author.html',{'profile':profile, 'user':user})

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
            profile.image = profile_form.cleaned_data['image']
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
        "<a href=/author/>here</a> to return to your profile.")
    else:
        return render_to_response('authors/manage.html',
            {'profile_form': profile_form}, context)

#Send Friend Request
def friend_request(request):
    if request.method == 'POST':
        to_profile_id = request.POST.get('to_profile','')
        current_profile = Profile.objects.get(user_id=request.user.id)
        to_profile = Profile.objects.get(id=to_profile_id)

        newFollow = Follow(from_profile_id=current_profile, to_profile_id=to_profile, status='PENDING')
        newFollow.save()
    return render(request, 'authors/index.html')

#Accept or Reject Friend Reject
def add_friend(request):
    current_profile = Profile.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        from_profile_id = request.POST.get('from_profile', '')

        if 'accept' in request.POST:
            current_profile.friends.add(Profile.objects.get(id=from_profile_id))
            current_profile.save()

            #Remove from follow
            qs = Follow.objects.filter(from_profile_id=from_profile_id).filter(to_profile_id=current_profile.id)
            qs.delete()

        elif 'reject' in request.POST:
            #change status form PENDING to REJECT
            qs = Follow.objects.filter(from_profile_id=from_profile_id).filter(to_profile_id=current_profile.id).update(status='REJECTED')
        return redirect('index')
    else:
        qs = Follow.objects.filter(to_profile_id=current_profile.id).filter(status='PENDING')
        if qs:
            friends = qs
        else:
            friends = None
        return render(request, 'authors/add_friend.html',{'friends':friends})
