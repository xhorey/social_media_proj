from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid
from datetime import datetime

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank_pfp.jpg')

    def __str__(self):
        return self.user.username
    

class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images', blank=True)
    text_of_post = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    no_of_likes = models.IntegerField(default=0)
    no_of_dislikes = models.IntegerField(default=0)
    no_of_reposts = models.IntegerField(default=0)
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    categories = models.ManyToManyField(Category, related_name="posts", blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return self.user.username
    
class DislikePost(models.Model):
    post_id = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dislikes")

    def __str__(self):
        return self.user.username

class FollowersCount(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")

    def __str__(self):
        return self.user.username
    
class Repost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reposts")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reposts")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    comment_text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

    
class KeyWord(models.Model):
    word = models.CharField(max_length=100, unique=True, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="keywords")

    def __str__(self):
        return self.word