from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.http import HttpResponse
from .models import Profile, Post, LikePost,DislikePost
from django.contrib.auth.decorators import login_required


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
def home(request):
    user_profile = Profile.objects.get(user=request.user)

    posts = Post.objects.all()
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
            user_profile.bi  = bio

            user_profile.save()

        return redirect('settings')
    
    return render(request, 'settings.html', {'user_profile': user_profile})

@login_required(login_url='signin')
def posting(request):
    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get('image')
        text_of_post = request.POST['postText']

        new_post = Post.objects.create(user=user, image=image, text_of_post=text_of_post)
        new_post.save()

        return redirect('/')
    else:
        return render(request, 'post.html')
    

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
    }
    return render(request, 'Profile.html', context)

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    dislike_filter = DislikePost.objects.filter(post_id=post_id, username=username).first()

    if dislike_filter != None:
        dislike_filter.delete()
        post.no_of_dislikes -= 1
        

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes += 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes -= 1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def dislike_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    dislike_filter = DislikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter != None:
        like_filter.delete()
        post.no_of_likes -= 1
        

    if dislike_filter == None:
        new_dislike = DislikePost.objects.create(post_id=post_id, username=username)
        new_dislike.save()
        post.no_of_dislikes += 1
        post.save()
        return redirect('/')
    else:
        dislike_filter.delete()
        post.no_of_dislikes -= 1
        post.save()
        return redirect('/')