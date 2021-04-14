
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post/<int:post_id>", views.posts, name="post"),
    path("createpost", views.createpost, name="createpost"),
    path("profile/<str:username>/<str:user>/", views.loadProfile, name="loadProfile"),
    path("following", views.following, name="following"),

    # API path
    path("follow", views.follow, name="follow"),
    path("editPost", views.editPost, name="editPost"),
    path("updateLike", views.updateLike, name="updateLike"), 
    path("getLikes/<int:postId>", views.getLikes, name="getLikes")
]
