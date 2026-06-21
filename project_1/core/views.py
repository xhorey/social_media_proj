from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from .models import Profile, Post, LikePost,DislikePost, FollowersCount, Comment, Hashtag, Repost, UserPreferences, UserPreferredCategory
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from itertools import chain
import json
import re

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
        
        

    else:
        return render(request, 'login.html')

@login_required(login_url='signin')
@never_cache
def home(request):
    user_profile = Profile.objects.get(user=request.user)

    posts = Post.objects.all().order_by('-created_at')

    for post in posts:
        post.latest_comments = post.comments.order_by('-created_at')[:2]

    return render(request, 'Main_Web_Page.html', {'user_profile': user_profile, 'posts':posts})

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']

        if confirmPassword == password:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken.')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken.')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signin')
        else:
            messages.info(request, 'Password is not matching!')
            return redirect('signup')

    else:

        return render(request, 'Signup.html')


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            user_profile.profileimg = image

        if request.FILES.get('banner') != None:
            banner = request.FILES.get('banner')
            user_profile.banner = banner

        
        user_profile.bio  = request.POST['bio']
        user_profile.save()

        return JsonResponse({'status': 'ok',
                             'bio': user_profile.bio,
                             'image_url': user_profile.profileimg.url,
                             'banner_url': user_profile.banner.url})
    
    return render(request, 'settings.html', {'user_profile': user_profile})


@login_required(login_url='signin')
def delete_post(request):
    if request.method == "POST":
        user = request.user
        data = json.loads(request.body)
        post_id = data.get('post_id')
        post = Post.objects.get(id = post_id)
        if post.user == user:
            post.delete()
        return JsonResponse({
            "success": True
        })

        


@login_required(login_url='signin')
def posting(request):

    user_profile = Profile.objects.get(user=request.user)

    if request.method == "POST":

        
        user = request.user
        image = request.FILES.get('image')
        text_of_post = request.POST['postText']
        aspect_ratio = request.POST.get('aspect_ratio', 'landscape')

        if image or text_of_post:

            new_post = Post.objects.create(
                user=user, 
                image=image, 
                text_of_post=text_of_post, 
                aspect_ratio=aspect_ratio
            )

            new_post.auto_assign_categories()
            new_post.auto_assign_hashtags()

            return redirect('/')
        
        else:
            messages.info(request, 'Post can not be empty!')
            return redirect('posting')

    else:
        return render(request, 'post.html', {'user_profile': user_profile})
    

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
@never_cache
def profile(request, pk):
    current_user = request.user
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=user_object)
    user_reposts = Repost.objects.filter(user=user_object, is_active = True)
    user_post_length = len(user_posts)
    amount_of_followers = len(FollowersCount.objects.filter(user=user_object))

    showed_posts = sorted(
        chain(user_posts, user_reposts),
        key=lambda instance: instance.created_at,
        reverse=True
    )

    for item in showed_posts:
        if isinstance(item, Repost):
            item.post.latest_comments = item.post.comments.order_by('-created_at')[:2]
        else:
            item.latest_comments = item.comments.order_by('-created_at')[:2]

    follower = request.user
    user = user_object

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'followers_count': amount_of_followers,
        'button_text': button_text,
        'posts_to_show': showed_posts,
        'current_user': current_user
    }
    return render(request, 'Profile.html', context)

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username

    user = User.objects.get(username=username)

    data = json.loads(request.body)
    post_id = data.get('post_id')

    post = get_object_or_404(Post, id=post_id)

    like_record, created = LikePost.objects.get_or_create(post_id=post_id, user=user)
    dislike_filter = DislikePost.objects.filter(post_id=post_id, user=user).first()

    if dislike_filter != None:
        dislike_filter.delete()
        post.no_of_dislikes -= 1
        

    if created or not like_record.is_active:

        post.no_of_likes += 1
        like_record.is_active = True

        if created:

            user_preferences, created = UserPreferences.objects.get_or_create(user=user)

            post_categories = post.categories.all()

            if post_categories.exists():
                for category in post_categories:

                    relationship, rel_created = UserPreferredCategory.objects.get_or_create(
                    preferences = user_preferences, 
                    category=category
                    )
                    
                    relationship.interest_score += 5
                    relationship.save()

    else:
        like_record.is_active = False
        post.no_of_likes -= 1

    post.save()
    like_record.save()

    return JsonResponse({
        "likes": post.no_of_likes,
        "dislikes": post.no_of_dislikes
    })

@login_required(login_url='signin')
def dislike_post(request):
    username = request.user.username

    user = User.objects.get(username=username)

    data = json.loads(request.body)
    post_id = data.get('post_id')

    post = get_object_or_404(Post, id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, user=user).first()
    dislike_filter = DislikePost.objects.filter(post_id=post_id, user=user).first()

    if like_filter != None and like_filter.is_active:
        like_filter.is_active = False
        post.no_of_likes -= 1
        

    if dislike_filter == None:
        DislikePost.objects.create(post_id=post_id, user=user)
        post.no_of_dislikes += 1
    else:
        dislike_filter.delete()
        post.no_of_dislikes -= 1

    post.save()
    like_filter.save()
    
    return JsonResponse({
        "likes": post.no_of_likes,
        "dislikes": post.no_of_dislikes
    })


@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.user
        username = request.POST['user'] 
        user = User.objects.get(username=username)

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            text_button = "Follow"
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            text_button = "Unfollow"

        amount_followers = len(FollowersCount.objects.filter(user=user))

        if amount_followers > 1:
            text_marker = "Followers"
        else:
            text_marker = "Follower"
        
        return JsonResponse({
            'text_button': text_button,
            'amount_followers': amount_followers,
            'text_marker': text_marker
        })

    else:
        return redirect('/')

@login_required(login_url='signin') 
def comment(request):
    user = request.user

    post_id = request.POST.get("post_id")
    post = Post.objects.filter(id=post_id).first()

    if not post:
        return JsonResponse({"status": "post not found"}, status=404)
    
    comment_text = request.POST.get("comment")

    Comment.objects.create(post=post, user=user, comment_text=comment_text)

    user_preferences, created = UserPreferences.objects.get_or_create(user=user)

    post_categories = post.categories.all()

    if post_categories.exists():
        for category in post_categories:

                relationship, rel_created = UserPreferredCategory.objects.get_or_create(preferences = user_preferences, category=category)

                relationship.interest_score += 25
                relationship.save()

    return JsonResponse({"status": "success",
                         "username": user.username,
                         "profile_img": user.profile.profileimg.url,
                         })

@login_required(login_url='signin')
def tag_posts(request, tag_name):
    posts = Post.objects.filter(
        hashtags__name=tag_name.lower()
    ).distinct().order_by('-created_at')

    for post in posts:
        post.latest_comments = post.comments.order_by('-created_at')[:2]

    user = request.user
    user_profile = Profile.objects.get(user=user)

    return render(
        request,
        "tag_posts.html",
        {"posts": posts, "tag": tag_name, 'user_profile':user_profile}
    )

@login_required(login_url='signin')
def search(request):
    query = request.GET.get("input_search", "")
    search_filter = request.GET.get("filter")
    user = request.user
    user_profile = Profile.objects.get(user=user)

    if search_filter == 'Post':

        content = Post.objects.filter(
            text_of_post__icontains=query
        ).order_by('-created_at') if query else Post.objects.none()

        if content.exists():
            for post in content:
                post.latest_comments = post.comments.order_by('-created_at')[:2]

    elif search_filter == 'User':

        content = Profile.objects.filter(
            user__username__icontains=query
        ) if query else Profile.objects.none()

        if content.exists():
            for profile in content:
                profile.number_of_followers = len(FollowersCount.objects.filter(user = profile.user))
                profile.number_of_posts = len(Post.objects.filter(user = profile.user))


    elif search_filter == 'Hashtag':

        content = Hashtag.objects.filter(
            name__icontains=query
        ) if query else Hashtag.objects.none()

        if content.exists():
            for tag in content:

                tag.number_posts = len(Post.objects.filter(
                hashtags__name=tag.name.lower()
                ).distinct())

        

    
    
    return render(request, "search.html", {'content': content, 'query':query, 'user_profile': user_profile, 'filter': search_filter})

@login_required(login_url='signin')
def repost(request):
    user = request.user
    data = json.loads(request.body)
    post_id = data.get('post_id')

    post = get_object_or_404(Post, id=post_id)

    if post.user != user:

        repost_filter, created = Repost.objects.get_or_create(post=post, user=user)

        if created or not repost_filter.is_active:

            if created:
            
                user_preferences, created = UserPreferences.objects.get_or_create(user=user)

                post_categories = post.categories.all()

                if post_categories.exists():
                    for category in post_categories:

                            relationship, rel_created = UserPreferredCategory.objects.get_or_create(preferences = user_preferences, category=category)

                            relationship.interest_score += 50
                            relationship.save()

            post.no_of_reposts += 1
            repost_filter.is_active = True


        else:
            repost_filter.is_active = False
            post.no_of_reposts -= 1

        post.save()
        repost_filter.save()

        return JsonResponse({
            "success": True,
            "no_reposts": post.no_of_reposts
        })
    else:
        return JsonResponse({
            "success": False,
            "message": "can't self repost",
            "no_reposts": post.no_of_reposts
        }, status=400)
