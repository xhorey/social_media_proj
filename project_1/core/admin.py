from django.contrib import admin
from .models import Profile, Post, LikePost, DislikePost, FollowersCount, Comment, Hashtag, Repost, Category, KeyWord, UserPreferredCategory, UserPreferences

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(DislikePost)
admin.site.register(FollowersCount)
admin.site.register(Comment)
admin.site.register(Hashtag)
admin.site.register(Repost)
admin.site.register(Category)
admin.site.register(KeyWord)
admin.site.register(UserPreferences)
admin.site.register(UserPreferredCategory)