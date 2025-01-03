from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json

from .models import *


def index(request):
    try:
        all_posts = Post.objects.all().order_by('-date_created')
        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get('page', 1)
        posts = paginator.get_page(page_number)
        followings = []
        suggestions = []
        if request.user.is_authenticated:
            followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
            suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        return render(request, "network/index.html", {
            "posts": posts,
            "suggestions": suggestions,
            "page": "all_posts",
            'profile': False
        })
    except Exception as e:
        return HttpResponse(status=500)


def login_view(request):
    try:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "network/login.html", {
                    "message": "Invalid username and/or password."
                })
        else:
            return render(request, "network/login.html")
    except Exception as e:
        return HttpResponse(status=500)


def logout_view(request):
    try:
        logout(request)
        return HttpResponseRedirect(reverse("index"))
    except Exception as e:
        return HttpResponse(status=500)


def register(request):
    try:
        if request.method == "POST":
            username = request.POST["username"]
            email = request.POST["email"]
            fname = request.POST["firstname"]
            lname = request.POST["lastname"]
            profile = request.FILES.get("profile")
            cover = request.FILES.get('cover')
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
            if password != confirmation:
                return render(request, "network/register.html", {
                    "message": "Passwords must match."
                })
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            if profile:
                user.profile_pic = profile
            else:
                user.profile_pic = "profile_pic/no_pic.png"
            user.cover = cover           
            user.save()
            Follower.objects.create(user=user)
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/register.html")
    except IntegrityError:
        return render(request, "network/register.html", {
            "message": "Username already taken."
        })
    except Exception as e:
        return HttpResponse(status=500)


def profile(request, username):
    try:
        user = User.objects.get(username=username)
        all_posts = Post.objects.filter(creater=user).order_by('-date_created')
        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get('page', 1)
        posts = paginator.get_page(page_number)
        followings = []
        suggestions = []
        follower = False
        if request.user.is_authenticated:
            followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
            suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
            if request.user in Follower.objects.get(user=user).followers.all():
                follower = True
        follower_count = Follower.objects.get(user=user).followers.all().count()
        following_count = Follower.objects.filter(followers=user).count()
        return render(request, 'network/profile.html', {
            "username": user,
            "posts": posts,
            "posts_count": all_posts.count(),
            "suggestions": suggestions,
            "page": "profile",
            "is_follower": follower,
            "follower_count": follower_count,
            "following_count": following_count
        })
    except Exception as e:
        return HttpResponse(status=500)


def following(request):
    try:
        if request.user.is_authenticated:
            following_user = Follower.objects.filter(followers=request.user).values('user')
            all_posts = Post.objects.filter(creater__in=following_user).order_by('-date_created')
            paginator = Paginator(all_posts, 10)
            page_number = request.GET.get('page', 1)
            posts = paginator.get_page(page_number)
            followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
            suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
            return render(request, "network/index.html", {
                "posts": posts,
                "suggestions": suggestions,
                "page": "following"
            })
        else:
            return HttpResponseRedirect(reverse('login'))
    except Exception as e:
        return HttpResponse(status=500)


def saved(request):
    try:
        if request.user.is_authenticated:
            all_posts = Post.objects.filter(savers=request.user).order_by('-date_created')
            paginator = Paginator(all_posts, 10)
            page_number = request.GET.get('page', 1)
            posts = paginator.get_page(page_number)
            followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
            suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
            return render(request, "network/index.html", {
                "posts": posts,
                "suggestions": suggestions,
                "page": "saved"
            })
        else:
            return HttpResponseRedirect(reverse('login'))
    except Exception as e:
        return HttpResponse(status=500)
        

@login_required
def create_post(request):
    try:
        if request.method == 'POST':
            text = request.POST.get('text')
            pic = request.FILES.get('picture')
            post = Post.objects.create(creater=request.user, content_text=text, content_image=pic)
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponse("Method must be 'POST'")
    except Exception as e:
        return HttpResponse(status=500)


@login_required
@csrf_exempt
def edit_post(request, post_id):
    try:
        if request.method == 'POST':
            text = request.POST.get('text')
            pic = request.FILES.get('picture')
            img_chg = request.POST.get('img_change')
            post_id = request.POST.get('id')
            post = Post.objects.get(id=post_id)
            post.content_text = text
            if img_chg != 'false':
                post.content_image = pic
            post.save()
            
            post_text = post.content_text if post.content_text else False
            post_image = post.img_url() if post.content_image else False
            
            return JsonResponse({
                "success": True,
                "text": post_text,
                "picture": post_image
            })
        else:
            return JsonResponse({"error": "Method must be 'POST'"}, status=405)
    except Exception as e:
        return HttpResponse(status=500)


@csrf_exempt
def like_post(request, id):
    try:
        if request.user.is_authenticated:
            if request.method == 'PUT':
                post = Post.objects.get(pk=id)
                post.likers.add(request.user)
                post.save()
                return HttpResponse(status=204)
            else:
                return HttpResponse("Method must be 'PUT'", status=405)
        else:
            return HttpResponseRedirect(reverse('login'))
    except Exception as e:
        return HttpResponse(status=500)


@csrf_exempt
def unlike_post(request, id):
    try:
        if request.user.is_authenticated:
            if request.method == 'PUT':
                post = Post.objects.get(pk=id)
                post.likers.remove(request.user)
                post.save()
                return HttpResponse(status=204)
            else:
                return HttpResponse("Method must be 'PUT'", status=405)
        else:
            return HttpResponseRedirect(reverse('login'))
    except Exception as e:
        return HttpResponse(status=500)


@csrf_exempt
def save_post(request, id):
    try:
        if request.user.is_authenticated:
            if request.method == 'PUT':
                post = Post.objects.get(pk=id)
                post.savers.add(request.user)
                post.save()
                return HttpResponse(status=204)
            else:
                return HttpResponse("Method must be 'PUT'", status=405)
        else:
            return HttpResponseRedirect(reverse('login'))
    except Exception as e:
        return HttpResponse(status=500)


@csrf_exempt
def unsave_post(request, id):
    try:
        if request.user.is_authenticated:
            if request.method == 'PUT':
                post = Post.objects.get(pk=id)
                post.savers.remove(request.user)
                post.save()
                return HttpResponse(status=204)
            else:
                return HttpResponse("Method must be 'PUT'", status=405)
        else:
            return HttpResponseRedirect(reverse('login'))
    except Exception as e:
        return HttpResponse(status=500)


@csrf_exempt
def follow(request, username):
    try:
        if request.user.is_authenticated:
            if request.method == 'PUT':
                user = User.objects.get(username=username)
                follower, created = Follower.objects.get_or_create(user=user)
                follower.followers.add(request.user)
                follower.save()
                return HttpResponse(status=204)
            else:
                return HttpResponse("Method must be 'PUT'", status=405)
        else:
            return HttpResponseRedirect(reverse('login'))
    except Exception as e:
        return HttpResponse(status=500)


@csrf_exempt
def unfollow(request, username):
    try:
        if request.user.is_authenticated:
            if request.method == 'PUT':
                user = User.objects.get(username=username)
                follower = Follower.objects.get(user=user)
                follower.followers.remove(request.user)
                follower.save()
                return HttpResponse(status=204)
            else:
                return HttpResponse("Method must be 'PUT'", status=405)
        else:
            return HttpResponseRedirect(reverse('login'))
    except Exception as e:
        return HttpResponse(status=500)


@csrf_exempt
def comment(request, post_id):
    try:
        if request.user.is_authenticated:
            if request.method == 'POST':
                data = json.loads(request.body)
                comment = data.get('comment_text')
                post = Post.objects.get(id=post_id)
                newcomment = Comment.objects.create(post=post, commenter=request.user, comment_content=comment)
                post.comment_count += 1
                post.save()
                return JsonResponse([newcomment.serialize()], safe=False, status=201)
            else:
                post = Post.objects.get(id=post_id)
                comments = Comment.objects.filter(post=post)
                comments = comments.order_by('-comment_time').all()
                return JsonResponse([comment.serialize() for comment in comments], safe=False)
        else:
            return HttpResponseRedirect(reverse('login'))
    except Exception as e:
        return HttpResponse(status=500)


@csrf_exempt
def delete_post(request, post_id):
    try:
        if request.user.is_authenticated:
            if request.method == 'PUT':
                post = Post.objects.get(id=post_id)
                if request.user == post.creater:
                    post.delete()
                    return HttpResponse(status=201)
                else:
                    return HttpResponse(status=404)
            else:
                return HttpResponse("Method must be 'PUT'", status=405)
        else:
            return HttpResponseRedirect(reverse('login'))
    except Exception as e:
        return HttpResponse(status=500)
