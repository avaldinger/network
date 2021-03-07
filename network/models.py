from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profilePicture = models.CharField(blank=True, max_length=255)
    followers = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
        }


class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    creationDate = models.DateTimeField(auto_now=True)
    post = models.TextField(blank=True)
    image = models.CharField(blank=True, max_length=255)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"Post id: {self.id}; created by: {self.username}"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username.username,
            "creationDate": self.creationDate.strftime("%b %d %Y, %I:%M %p"),
            "post": self.post,
            "image": self.image,
            "likes": self.likes
        }

class Like(models.Model):
    likedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Like id: {self.id}; Liked by: {self.likedBy}"
    
    def serialize(self):
        return {
            "id": self.id,
            "likedBy": self.likedBy,
            "liked": self.liked,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

class Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, )
    post =  models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment id: {self.id}; Commented by: {self.username} at {self.timestamp}"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "post": self.post,
            "comment": self.comment,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

class Follow(models.Model):
    user = models.IntegerField()
    followedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} followed by: {self.followedBy} at {self.timestamp}"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "followedBy": self.followedBy,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

    
