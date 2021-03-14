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

from .models import User, Post, Follow

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


def index(request):
    # Form to create post
    form =  PostForm()
    # Get all existing posts
    posts = Post.objects.all().order_by('-creationDate')
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

def posts(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post doesn't exixts"}, status = 404)
    return JsonResponse(post.serialize())


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

def loadProfile(request, username):
    # Get profile
    userInfo = User.objects.get(username=username)
    # Check if profile followed by the user
    followed = Follow.objects.filter(followedBy=userInfo.id)
    # Get posts for the profile
    posts = Post.objects.filter(username=userInfo.id).order_by('-creationDate')
    return render(request, "network/profile.html", {
        "posts": posts, "userInfo": userInfo, "followed": followed
    })

@csrf_exempt
def follow(request):
    print("following")
    print(request.method)
    body_unicode = request.body.decode('utf-8')
    print(request.body)
    # data = json.loads(request.body)
    # print(data)
    return HttpResponse("JSON received...")
    # return redirect('loadProfile', username=username)



def following(request):
    user = request.user
    followed = Follow.objects.filter(followedBy=user.id)
    print(followed)
    return render(request, "network/following.html")
