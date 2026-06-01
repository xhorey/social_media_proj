from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.http import HttpResponse
from .models import Profile, Post, LikePost,DislikePost, FollowersCount, Comment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
import json

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
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']

            user_profile.profileimg = image
            user_profile.bio = bio

            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']

            user_profile.profileimg = image
            user_profile.bio  = bio

            user_profile.save()

        return JsonResponse({'status': 'ok',
                             'bio': user_profile.bio,
                             'image_url': user_profile.profileimg.url})
    
    return render(request, 'settings.html', {'user_profile': user_profile})

@login_required(login_url='signin')
def posting(request):

    user_profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        user = request.user
        image = request.FILES.get('image')
        text_of_post = request.POST['postText']

        

        new_post = Post.objects.create(user=user, image=image, text_of_post=text_of_post)
        new_post.save()

        return redirect('/')
    else:
        return render(request, 'post.html', {'user_profile': user_profile})
    

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
@never_cache
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=user_object)
    user_post_length = len(user_posts)
    amount_of_followers = len(FollowersCount.objects.filter(user=user_object))

    showed_posts = user_posts.order_by('-created_at')

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
    }
    return render(request, 'Profile.html', context)

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username

    data = json.loads(request.body)
    post_id = data.get('post_id')

    post = get_object_or_404(Post, id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    dislike_filter = DislikePost.objects.filter(post_id=post_id, username=username).first()

    if dislike_filter != None:
        dislike_filter.delete()
        post.no_of_dislikes -= 1
        

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes += 1
    else:
        like_filter.delete()
        post.no_of_likes -= 1

    post.save()

    return JsonResponse({
        "likes": post.no_of_likes,
        "dislikes": post.no_of_dislikes
    })

@login_required(login_url='signin')
def dislike_post(request):
    username = request.user.username

    data = json.loads(request.body)
    post_id = data.get('post_id')

    post = get_object_or_404(Post, id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    dislike_filter = DislikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter != None:
        like_filter.delete()
        post.no_of_likes -= 1
        

    if dislike_filter == None:
        new_dislike = DislikePost.objects.create(post_id=post_id, username=username)
        new_dislike.save()
        post.no_of_dislikes += 1
    else:
        dislike_filter.delete()
        post.no_of_dislikes -= 1

    post.save()
    
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

    new_comment = Comment.objects.create(post=post, user=user, comment_text=comment_text)
    new_comment.save()

    return JsonResponse({"status": "success"})

