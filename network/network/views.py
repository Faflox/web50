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
    logged_in_user = request.user
    posts = Post.objects.all().order_by("-date")
    
    if logged_in_user.is_authenticated:
        is_following = Followers.objects.filter(user_id = logged_in_user.id).values_list('follower_id', flat=True) 
        is_liking =  Like.objects.filter(user = logged_in_user).values_list('post', flat=True)
    else:
        is_following = []
        is_liking = []
    
    posts = Post.objects.all().order_by("-date")
    p = Paginator(posts, 10)
    page = request.GET.get('page')
    posts_paginated = p.get_page(page)
    return render(request, "network/index.html", {
        "posts": posts, 
        "posts_paginated": posts_paginated,
        "is_following": is_following,
        "is_liking": is_liking})

def following(request):
    logged_in_user = request.user

    following = logged_in_user.is_following.all().values_list('follower_id', flat=True)
    
    posts = Post.objects.filter(user__id__in=following) | Post.objects.filter(user=request.user)

    is_following = Followers.objects.filter(user_id = logged_in_user.id).values_list('follower_id', flat=True) 
    
    posts = Post.objects.filter(user__id__in=is_following) | Post.objects.filter(user=request.user)

    posts.order_by("-date") 
    p = Paginator(posts, 10)
    page = request.GET.get('page')
    posts_paginated = p.get_page(page)

    return render(request, "network/following.html", {
        "posts": posts, 
        "posts_paginated": posts_paginated})


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
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

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
                user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name, profilePicture=profilePicture)
            else:
                profilePicture = settings.STATIC_URL + 'images/default.jpeg'
                user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name, profilePicture=profilePicture) 
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
    logged_in_user = request.user
    if not user_profile_info.profilePicture:
        user_profile_info.profilePicture = settings.STATIC_URL + 'images/default.jpg'
        
    if logged_in_user.is_authenticated:
        is_following = Followers.objects.filter(user_id = logged_in_user.id).values_list('follower_id', flat=True) 
        is_liking =  Like.objects.filter(user = logged_in_user).values_list('post', flat=True)
    else:
        is_following = []
        is_liking = []
        
    #next line retrieves posts associated with the current user 
    user_posts = Post.objects.filter(user=user_profile_info).order_by("-date")    
    
    return render(request, "network/profile.html", {
        'user_profile_info': user_profile_info, 
        'posts': user_posts, 
        'logged_in_user': request.user,
        'is_following': is_following,
        'is_liking': is_liking})


def edit_description(request, username):
    user_profile_info = User.objects.get(username=username)
    data = json.loads(request.body)
    new_description = data.get("content")
    if new_description:
        user_profile_info.description = new_description
        user_profile_info.save()
    
    return render(request, "network/profile.html")

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
def edit_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content")
        post_id = data.get("post_id")
        post = Post.objects.filter(id=post_id).first()
        
        if post is None:
            return JsonResponse({'status': 'error', 'message': 'Invalid post ID'})
        post.content = content
        post.save()
        return JsonResponse({'status': 'success', 'message': 'Post edited successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
 
@csrf_exempt
@login_required       
def delete_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get("post_id")
        post = Post.objects.filter(id=post_id).first()
        
        if post is None:
            return JsonResponse({'status': 'error', 'message': 'Invalid post ID'})
        post.delete()
        return JsonResponse({'status': 'success', 'message': 'Post deleted successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
@login_required   
def like(request):
    if request.method == "POST":
        data = json.loads(request.body)
        action_post_id = data.get("content")
        action_post = Post.objects.filter(id=action_post_id).first()
        logged_in_user = request.user
        
        if action_post is None:
            return JsonResponse({'status': 'error', 'message': 'Invalid post ID'})
        
        if Like.objects.filter(user = logged_in_user, post = action_post_id).exists():
            Like.objects.filter(user = logged_in_user, post = action_post_id).delete()
            return JsonResponse({'status': 'unliked'})
        else: 
            Like.objects.create(user = logged_in_user, post = action_post)
            return JsonResponse({'status': 'liked'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
            
            

@csrf_exempt
@login_required
def follow_unfollow(request):
    if request.method == "POST":
        data = json.loads(request.body)
        action_profile_id = data.get("content")
        action_profile = User.objects.get(id=action_profile_id)
        logged_in_user_id = request.user
        

        # Check if the user is already following the profile
        if Followers.objects.filter(user_id=logged_in_user_id, follower_id=action_profile_id).exists():
            Followers.objects.filter(user_id=logged_in_user_id, follower_id=action_profile_id).delete()
            return JsonResponse({'status': 'unfollowed'})
        else:
            Followers.objects.create(user_id=logged_in_user_id, follower_id=action_profile)
            return JsonResponse({'status': 'followed'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


    

