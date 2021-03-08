from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from .models import User, Post

class PostForm(forms.ModelForm):
    # description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        exclude = ['username', 'creationDate', 'likes']
        widgets = {
            'post': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'style': 'width: 100%'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
            'description', css_class='form-group col-md-7 mb-0',
            ),
            Submit('submit', 'Post')
        )


def index(request):
    form =  PostForm()
    posts = Post.objects.all()
    username = request.user
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
    return HttpResponse("From Received")
