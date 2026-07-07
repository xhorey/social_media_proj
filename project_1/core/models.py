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
    banner = models.ImageField(upload_to='banners', default='default_banner.png')

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
    ASPECT_RATIO_CHOICES = [
        ('landscape', 'Landscape (1.91:1)'),
        ('square', 'Square (1:1)'),
        ('portrait', 'Portrait (9:16)'),
    ]
    aspect_ratio = models.CharField(
        max_length=20, 
        choices=ASPECT_RATIO_CHOICES, 
        default='landscape' # fallback to your current design
    )

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

    is_active = models.BooleanField(default=True)

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

    is_active = models.BooleanField(default=True)

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
    
class UserPreferences(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="preferences")
    
    categories = models.ManyToManyField(Category, through='UserPreferredCategory', blank=True)

    last_decay = models.DateTimeField(default=timezone.now)

    DECAY_RATE = 0.99

    def call_decay(self):
        now = timezone.now()
        time_passed = now - self.last_decay
        twelve_hours_passed = time_passed.total_seconds() / 3600 / 12
        if twelve_hours_passed >= 1:
            for preferred_category in self.preferred_categories.all():
                preferred_category.interest_score *= self.DECAY_RATE ** twelve_hours_passed
                if preferred_category.interest_score < 0.01:
                    preferred_category.interest_score = 0
                preferred_category.save()

            self.last_decay = now
            self.save()
            

    def __str__(self):
        return f"{self.user.username}"

class UserPreferredCategory(models.Model):
    preferences = models.ForeignKey(UserPreferences, on_delete=models.CASCADE, related_name="preferred_categories")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    interest_score = models.FloatField(default=0) 
    last_interacted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.preferences.user.username} - {self.category.name} ({self.interest_score})"