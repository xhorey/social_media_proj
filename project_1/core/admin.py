from django.contrib import admin
from .models import Profile, Post, LikePost, DislikePost, FollowersCount, Comment, Hashtag

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(DislikePost)
admin.site.register(FollowersCount)
admin.site.register(Comment)
admin.site.register(Hashtag)