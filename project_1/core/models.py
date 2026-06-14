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

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)

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
    
    def auto_assign_categories(self):
        import re
        words = re.findall(r'\b\w+\b', self.text_of_post.lower())
        if words:
            from .models import KeyWord

            search_terms = set(words)

            for i in range(len(words) - 1):
                search_terms.add(f"{words[i]} {words[i+1]}")

            for i in range(len(words) - 2):
                search_terms.add(f"{words[i]} {words[i+1]} {words[i+2]}")

            matched_kws = KeyWord.objects.filter(word__in=search_terms).select_related('category')
            categories_to_add = {kw.category for kw in matched_kws}
            if categories_to_add:
                self.categories.add(*categories_to_add)


    def auto_assign_hashtags(self):
        import re
        tags = re.findall(r"#(\w+)", self.text_of_post.lower()) 
        if tags:
            hashtags_to_add = []
            from .models import Hashtag
            for tag in tags:
                hashtag, created = Hashtag.objects.get_or_create(name = tag.lower())
                hashtags_to_add.append(hashtag)

            self.hashtags.add(*hashtags_to_add)



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

    def save(self, *args, **kwargs):
        self.word = self.word.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.word