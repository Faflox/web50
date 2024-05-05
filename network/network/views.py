import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Like, Followers


def index(request):
    posts = Post.objects.all().order_by("-date")
    p = Paginator(posts, 10)
    page = request.GET.get('page')
    posts_paginated = p.get_page(page)
    return render(request, "network/index.html", {"posts": posts, "posts_paginated": posts_paginated})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            if 'profilePicture' in request.FILES:
                profilePicture = request.FILES['profilePicture']
                user = User.objects.create_user(username, email, password, profilePicture=profilePicture)
            else:
                profilePicture = settings.STATIC_URL + 'images/default.jpeg'
                user = User.objects.create_user(username, email, password, profilePicture=profilePicture) 
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")



def profile(request, username):
    #create a variable user_profile_info that has the  data from the user that has the username provided from request
    user_profile_info = User.objects.get(username=username)
    if not user_profile_info.profilePicture:
        user_profile_info.profilePicture = settings.STATIC_URL + 'images/default.jpg'
        
    #next line retrieves posts associated with the current user 
    user_posts = Post.objects.filter(user=user_profile_info).order_by("-date")
    
    return render(request, "network/profile.html", {'user_profile_info': user_profile_info, 'posts': user_posts, 'logged_in_user': request.user})


@csrf_exempt
@login_required
def create_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content")
        if content:
            Post.objects.create(user=request.user, content=content)
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def follow_unfollow(request):
    if request.method == "POST":
        data = json.loads(request.body)
        action_profile = data.get("content")
        logged_in_user = request.user

        # Check if the user is already following the profile
        if Followers.objects.filter(user_id=logged_in_user, follower_id=action_profile).exists():
            # If the follow relationship exists, delete it (unfollow)
            Followers.objects.filter(user_id=logged_in_user, follower_id=action_profile).delete()
            return JsonResponse({'status': 'unfollowed'})
        else:
            # If the follow relationship doesn't exist, create it (follow)
            Followers.objects.create(user_id=logged_in_user, follower_id=action_profile)
            return JsonResponse({'status': 'followed'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def following(request):
    #retrieve currently logged user's info
    logged_in_user = request.user
    #retrieve from Followers model list where user_id = logged_in_user
    following = logged_in_user.is_following.all().values_list('follower_id', flat=True)
    #retrieve from Post where foreign key user
    posts = Post.objects.filter(user__id__in=following).order_by("-date")
    
    #set up paginator
    p = Paginator(posts, 10)
    page = request.GET.get('page')
    posts_paginated = p.get_page(page)
    return render(request, "network/following.html", {"posts": posts, "posts_paginated": posts_paginated})




    

