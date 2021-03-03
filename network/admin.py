from django.contrib import admin

from .models import User, Post, Comment, Like, Follow

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "creationDate", "post", "likes")
    # list_editable = ("item", "description", "category", "sold", "price", "image", "bidWinner", "createdBy")

class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "likedBy", "post", "liked", "timestamp")
    # list_editable = ("currentBid", "nextBid")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "comment", "username", "post", "timestamp")
    # list_editable = ("comment",)

class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "followedBy", "timestamp")



admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Follow, FollowAdmin) 
