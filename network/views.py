from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import User, Post, Follow, Like

# Input form for creating a new Post
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ['username', 'creationDate', 'likes']
        widgets = {
            'post': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'style': 'width: 100%'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs["placeholder"] = "Best title.."
        self.fields["title"].widget.attrs["autocomplete"] = "off"
        self.fields["title"].required = True
        self.fields["post"].widget.attrs["placeholder"] = "What are you thinking?"
        self.fields["post"].widget.attrs["autocomplete"] = "off"
        self.fields["post"].required = True
        self.fields["image"].widget.attrs["placeholder"] = "Add a fancy Image!"
        self.fields["image"].widget.attrs["autocomplete"] = "off"
        self.fields["image"].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
            'image', css_class='form-group col-md-6 mb-0',
            ),
            Row(
            'title', css_class='form-group col-md-7 mb-0',
            ),
            Row(
            'description', css_class='form-group col-md-7 mb-0',
            ),
            Submit('submit', 'Post')
        )

@login_required
def index(request):
    # Form to create post
    form =  PostForm()
    # Get all existing posts
    all_posts = Post.objects.all().order_by('-creationDate')
    # Paginate posts
    paginator = Paginator(all_posts, 10)
    # Get page number
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)
    # print(posts)
    username = request.user
    # Get User info to use in the HTML
    user = User.objects.get(username=username.username)
    return render(request, "network/index.html", {
        "posts": posts, "user": user, "form": form
    })


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
    return render(request, "network/login.html")


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
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def posts(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post doesn't exixts"}, status = 404)
    return JsonResponse(post.serialize())

@login_required
def createpost(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        username = request.user
        # Check form and save entry to the DataBase
        if form.is_valid():
            post = form.cleaned_data["post"]
            image = form.cleaned_data["image"]
            title = form.cleaned_data["title"]
            newPost = Post(post=post,  image=image, title=title, creationDate=datetime.now(), username=username)
            newPost.save()
            return redirect('index')
            # return HttpResponse("Post saved")
        return HttpResponse("Incorrect input")
    return HttpResponse("From Received")

@login_required
def loadProfile(request, username, user):
    # Get profile
    # print("Loading profile...")
    userInfo = User.objects.get(username=username)
    follower = User.objects.get(username=user)
    # Check if profile followed by the user
    followed = Follow.objects.filter(user=userInfo.id, followedBy=follower)
    followedBy = ""
    # print(f"Followedby: {followed}")
    if followed:
        followedBy = followed[0]
    # Get posts for the profile
    all_posts = Post.objects.filter(username=userInfo.id).order_by('-creationDate')
    # Paginate posts
    paginator = Paginator(all_posts, 10)
    # Get page number
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        "posts": posts, "userInfo": userInfo, "followed": followedBy
    })

@csrf_exempt
def follow(request):
    # Get JSON Object passed by the JS function from the front-end
    data = json.loads(request.body)
    # print(data["user"])
    # print(data["followedBy"])
    username = User.objects.get(pk=data["user"])
    # print(username)
    followedBy = User.objects.filter(id=data["followedBy"])
    # print(followedBy[0].username)
    follower = followedBy[0].username
    # Add entry to DB if following
    if data["status"] == "follow":
        newFollow = Follow(user=data["user"], followedBy=followedBy[0], timestamp=datetime.now())
        newFollow.save()
        # print("saved")
    # Remove entry from DB if unfollowing
    if data["status"] == "unfollow":
        Follow.objects.filter(user=data["user"], followedBy=followedBy[0]).delete()
        # print("deleted")
    # return HttpResponse("JSON received...")
    return redirect('loadProfile', username=username, user=follower)


@login_required
def following(request):
    # Get the user
    user = request.user
    # List to store all posters followed by current user
    userids = []
    # Get which posters the user is following
    followed = Follow.objects.filter(followedBy=user.id)
    for posters in followed:
        # Add them into a list
        userids.append(posters.user)   
    # Query posts which created by posters who the user is following 
    all_posts = Post.objects.filter(username__in=userids)
    # Paginate posts
    paginator = Paginator(all_posts, 10)
    # Get page number
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "posts": posts
    })

@csrf_exempt
@login_required
def editPost(request):
    # Get the user
    user = request.user
    print(user)
    # Get JSON Object passed by the JS function from the front-end
    data = json.loads(request.body)
    print(data)
    print(data["user"])
    username = User.objects.get(pk=data["user"])
    print(username.id)
    if user == username:
        # Update post text in the DataBase
        Post.objects.filter(pk=data["postId"]).update(post=data["post"])
        return HttpResponse(status=204)
    return HttpResponse(status=400)

@csrf_exempt
@login_required
def updateLike(request):
    # Get JSON Object passed by the JS function from the front-end
    data = json.loads(request.body)
    print(data)
    username = User.objects.get(pk=data["user"])
    post = Post.objects.get(pk=data["postId"])
    counter = data["counter"]
    currentLikes = post.likes
    print(currentLikes)
    if counter > 0:
        currentLikes += 1
        Post.objects.filter(pk=data["postId"]).update(likes=currentLikes)
        liked = Like(likedBy=username, post=post, liked=True, timestamp=datetime.now())
        liked.save()
        return HttpResponse(status=204)
    else:
        currentLikes -= 1
        print(currentLikes)
        Post.objects.filter(pk=data["postId"]).update(likes=currentLikes)
        Like.objects.filter(likedBy=username, post=post).delete()
        return HttpResponse(status=204)
    return HttpResponse(status=400)

@csrf_exempt
@login_required
def getLikes(request, postId):

    try:
        post = Post.objects.get(pk=postId)
    except Post.DoesNotExist:
        return JsonResponse({"error: Post with id {postId} doesn't exists"}, status=404)

    return JsonResponse(post.serialize())
    

