from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from .models import Profile, Post, LikePost,DislikePost, FollowersCount, Comment, Hashtag, Repost, UserPreferences, UserPreferredCategory
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.db.models import Count, Prefetch
from uuid import UUID
from itertools import chain
from collections import deque
import json
import random
from django.utils import timezone
import math

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

    followed_users = set(
        FollowersCount.objects.filter(follower=request.user)
        .values_list("user_id", flat=True)
    )

    preferences, created = UserPreferences.objects.get_or_create(
    user=request.user)

    preferences.call_decay()
    
    preferred_categories = UserPreferredCategory.objects.filter(preferences=preferences)

    preference_scores = {
        pref.category_id: pref.interest_score
        for pref in preferred_categories
    }
    max_category_score = 0
    if preference_scores:

        max_interest = max(preference_scores.values())

        if max_interest > 0:
            preference_scores = {
                category_id: score / max_interest
                for category_id, score in preference_scores.items()
            }
    
            max_category_score = sum(preference_scores.values())

    top_categories = preferred_categories.order_by('-interest_score')[:3]
    top_category_ids = top_categories.values_list('category_id',flat=True)

    other_categories = preferred_categories.exclude(category__id__in=top_category_ids)

    print("Categories have been selected.")

    posts = []
    selected_post_ids = set()
    now = timezone.now()
    random_in_sequence = 0

    latest_comments = Prefetch(
        "comments",
        queryset=Comment.objects.select_related("user").order_by("-created_at"),
        to_attr="prefetched_comments",
    )

    def can_add_post(post):
        if post.id in selected_post_ids:
            return False

        if posts:
            last_user = posts[-1].user

            if post.user == last_user:

                remaining_posts = (list(top_posts) + list(other_posts) + list(random_posts))

                has_other_user = any(
                    p.user.id != last_user.id and p.id not in selected_post_ids
                    for p in remaining_posts
                )

                if has_other_user:
                    return False

        return True

    def get_valid_post(queue):
        for post in list(queue):
            if can_add_post(post):
                if add_post(post):
                    queue.remove(post)
                
                    return post

        return None

    def add_post(post):
        nonlocal posts, selected_post_ids

        if post.id in selected_post_ids:
            return False

        posts.append(post)
        selected_post_ids.add(post.id)
        return True

    def score_post(post, is_random):
        hours_old = (now - post.created_at).total_seconds() / 3600
        post_freshness = math.exp(-hours_old / 72)
        likes_count = post.no_of_likes
        comments_count = post.comment_count
        reposts_count = post.no_of_reposts
        popularity = math.log(likes_count + comments_count + reposts_count + 1)
        if not is_random:
            category_score = 0

            for category in post.categories.all():
                category_score += preference_scores.get(category.id, 0)

            if max_category_score > 0:
                category_score_norm = category_score / max_category_score
            else:
                category_score_norm = 0

        popularity_norm = min(
            popularity / math.log(1000 + 1),
            1
        )
        if not is_random:

            post.score = (
                0.5 * category_score_norm +
                0.3 * popularity_norm +
                0.2 * post_freshness
            )

        else:

            post.score = (
                0.6 * popularity_norm +
                0.4 * post_freshness
            )

        author_id = post.user.id

        if author_id in followed_users:
            post.score *= 1.5

        post.score *= random.uniform(0.98, 1.02)

    print("Functions initialized.")

    if request.method == 'POST':

        body = json.loads(request.body)

        loaded_posts = body.get("loaded_posts", [])

        loaded_posts = [UUID(x) for x in loaded_posts]

        top_posts = (
            Post.objects
            .exclude(id__in=loaded_posts)
            .filter(categories__id__in=top_category_ids)
        )
        for post in top_posts:
            score_post(post=post, is_random=False)
        top_posts = sorted(top_posts, key=lambda post: post.score, reverse=True)
        top_posts = deque(top_posts)
        other_posts = Post.objects.exclude(id__in=loaded_posts).filter(categories__id__in=other_categories.values_list('category_id', flat=True)).distinct().annotate(comment_count=Count("comments")).select_related("user").prefetch_related("categories",  latest_comments)
        for post in other_posts:
            score_post(post=post, is_random=False)

        other_posts = sorted(other_posts, key=lambda post: post.score, reverse=True)

        other_posts = deque(other_posts)
        random_posts = (Post.objects.exclude(id__in=loaded_posts).exclude(categories__id__in=preferred_categories.values_list("category_id", flat=True)).distinct().annotate(comment_count=Count("comments"))).select_related("user").prefetch_related("categories",  latest_comments)

        for post in random_posts:
            score_post(post=post, is_random=True)

        random_posts = sorted(random_posts, key=lambda post: post.score, reverse=True)

        random_posts = deque(random_posts)

        while len(posts)<30 and (top_posts or other_posts or random_posts):
            r = random.random()

            if random_in_sequence <2:

                if r < 0.60 and top_posts:
                    post = get_valid_post(top_posts)

                    if post:
                        random_in_sequence = 0

                elif r < 0.83 and other_posts:
                    post = get_valid_post(other_posts)
                    if post:
                        random_in_sequence = 0

                elif random_posts:
                    post = get_valid_post(random_posts)
                    if post:
                        random_in_sequence += 1
                else:
                    if top_posts:
                        post = get_valid_post(top_posts)
                        if post:
                            random_in_sequence = 0
                    elif other_posts:
                        post = get_valid_post(other_posts)
                        if post:
                            random_in_sequence = 0
                    else:
                        break

                        

            else:
                if r <= 0.70 and top_posts:
                    post = get_valid_post(top_posts)
                    if post:
                        random_in_sequence = 0
                    else:
                        print(f"Didn't get the post, trying other. remains:{len(other_posts)}")
                        post = get_valid_post(other_posts)
                        if post:
                            print("Got other post succesfully")
                            random_in_sequence = 0
                        else:
                            print(f"Failed to get any post. Remaining options: {len(other_posts) + len(top_posts) + len(random_posts)}\nForced random post...")
                            post = get_valid_post(random_posts)
                            if post:
                                print("Got forced random succesfully!")
                elif r > 0.70 and other_posts:
                    post = get_valid_post(other_posts)
                    if post:
                        random_in_sequence = 0
                    else:
                        print("Didn't get the post, trying top")
                        post = get_valid_post(top_posts)
                        if post:
                            print("Got top post succesfully")
                            random_in_sequence = 0
                        else:
                            print(f"Failed to get any post. Remaining options: {len(other_posts) + len(top_posts) + len(random_posts)}\n Forced random...")
                            post = get_valid_post(random_posts)
                            if post:
                                print("Got forced random succesfully!")
                else:
                    if random_posts:
                        post = get_valid_post(random_posts)
                        if post:
                            random_in_sequence += 1 
                    else:
                        if top_posts:
                            post = get_valid_post(top_posts)
                            if post:
                                random_in_sequence = 0
                        elif other_posts:
                            post = get_valid_post(other_posts)
                            if post:
                                random_in_sequence = 0
                        else:
                            break


        for post in posts:
            post.latest_comments = post.prefetched_comments[:2]

        ids = [post.id for post in posts]

        print(f"Total posts: {len(ids)}")
        print(f"Unique posts: {len(set(ids))}")

        return JsonResponse({
            "posts": [
                {
                    "id": str(post.id),
                    "username": post.user.username,
                    "profile": post.user.profile.profileimg.url,
                    "text": post.text_of_post,
                    "likes": post.no_of_likes,
                    "dislikes": post.no_of_dislikes,
                    "created": post.created_at.isoformat(),
                    "aspect_ratio": post.aspect_ratio,
                    "image_url": post.image.url if post.image else None,
                    "reposts": post.no_of_reposts,
                    "comments": [
                        {
                            "username": comment.user.username,
                            "profile": comment.user.profile.profileimg.url,
                            "text": comment.comment_text,
                        }
                        for comment in post.latest_comments
                    ],
                    "is_owner": post.user == request.user,

                }
                for post in posts
            ]
        })

    print("If POST has been passed.")

    top_posts = Post.objects.filter(categories__id__in =top_category_ids).distinct().annotate(comment_count=Count("comments")).select_related("user").prefetch_related("categories",  latest_comments)
    for post in top_posts:
        score_post(post=post, is_random=False)


    top_posts = sorted(top_posts, key=lambda post: post.score, reverse=True)

    top_posts = deque(top_posts)

    other_posts = Post.objects.filter(categories__id__in=other_categories.values_list('category_id', flat=True)).distinct().annotate(comment_count=Count("comments")).select_related("user").prefetch_related("categories",  latest_comments)

    for post in other_posts:
        score_post(post=post, is_random=False)

    other_posts = sorted(other_posts, key=lambda post: post.score, reverse=True)

    other_posts = deque(other_posts)

    random_posts = (Post.objects.exclude(categories__id__in=preferred_categories.values_list("category_id", flat=True)).distinct().annotate(comment_count=Count("comments"))).select_related("user").prefetch_related("categories",  latest_comments)

    for post in random_posts:
        score_post(post=post, is_random=True)

    random_posts = sorted(random_posts, key=lambda post: post.score, reverse=True)

    random_posts = deque(random_posts)

    print("Buckets created.")

    print("Starting loop.")

    while len(posts)<30 and (top_posts or other_posts or random_posts):
        r = random.random()

        if random_in_sequence <2:

            print("Random is < 2")

            if r < 0.60 and top_posts:
                print("Trying to get top post")
                post = get_valid_post(top_posts)

                if post:
                    print("Got top post succesfully")
                    random_in_sequence = 0
                else:
                    print("Didn't get the top, trying other...")
                    post = get_valid_post(other_posts)
                    if post:
                        print("Got other post succesfully")
                        random_in_sequence = 0
                    else:
                        print("Didn't get other post. Forced random...")
                        post = get_valid_post(random_posts)
                        if post:
                            print("Succes")
                        else:
                            print("FAILED. CRITICAL.")


            elif r < 0.83 and other_posts:
                print("Trying to get other post")
                post = get_valid_post(other_posts)
                if post:
                    print("Got other post succesfully")
                    random_in_sequence = 0
                else:
                    print("Didn't get the other, trying top...")
                    post = get_valid_post(top_posts)
                    if post:
                        print("Got top post succesfully")
                        random_in_sequence = 0
                    else:
                        print("Didn't get top post. Forced random...")
                        post = get_valid_post(random_posts)
                        if post:
                            print("Succes")
                        else:
                            print("FAILED. CRITICAL.")

                

            elif random_posts:
                print("Trying to get random post")
                post = get_valid_post(random_posts)
                if post:
                    print("Got random post succesfully")
                    random_in_sequence += 1
            else:
                if top_posts:
                    print("Trying to get top post")
                    post = get_valid_post(top_posts)
                    if post:
                        print("Got top post succesfully")
                        random_in_sequence = 0
                    else:
                        print("Failed")
                        pass
                elif other_posts:
                    print("Trying to get other post")
                    post = get_valid_post(other_posts)
                    if post:
                        print("Got other post succesfully")
                        random_in_sequence = 0
                else:
                    break

                    

        else:
            print("two randoms in a row")
            if r <= 0.70 and top_posts:
                print(f"Trying to get top post. remains:{len(top_posts)}")
                post = get_valid_post(top_posts)
                if post:
                    print("Got top post succesfully")
                    random_in_sequence = 0
                else:
                    print(f"Didn't get the post, trying other. remains:{len(other_posts)}")
                    post = get_valid_post(other_posts)
                    if post:
                        print("Got other post succesfully")
                        random_in_sequence = 0
                    else:
                        print(f"Failed to get any post. Remaining options: {len(other_posts) + len(top_posts) + len(random_posts)}\nForced random post...")
                        post = get_valid_post(random_posts)
                        if post:
                            print("Got forced random succesfully!")

            elif r > 0.70 and other_posts:
                print("Trying to get other post")
                post = get_valid_post(other_posts)
                if post:
                    print("Got other post succesfully")
                    random_in_sequence = 0
                else:
                    print("Didn't get the post, trying top")
                    post = get_valid_post(top_posts)
                    if post:
                        print("Got top post succesfully")
                        random_in_sequence = 0
                    else:
                        print(f"Failed to get any post. Remaining options: {len(other_posts) + len(top_posts) + len(random_posts)}\n Forced random...")
                        post = get_valid_post(random_posts)
                        if post:
                            print("Got forced random succesfully!")
            else:
                print("Only random posts available")
                if random_posts:
                    print("Trying to get random post")
                    post = get_valid_post(random_posts)
                    if post:
                        print("Got random post succesfully")
                        random_in_sequence += 1 
                else:
                    print(f"Got all posts remains: {len(other_posts) + len(top_posts) + len(random_posts)}")
                    break

    
    print("Loop escaped.")

    for post in posts:
        post.latest_comments = post.prefetched_comments[:2]

    # print("Top catetorys:\n")
    # for category in top_categories:
    #     print(category)
    #     print(category.interest_score)
    # print("Others:\n")
    # for category in other_categories:
    #     print(category)
    #     print(category.interest_score)
    # print("Posts showed:\n")
    # for post in posts:
    #     print("Post:", post.id)
    #     print("score:", post.score)
    #     for category in post.categories.all():
    #         print(category)

    # print(f"Total is {len(posts)}")

    ids = [post.id for post in posts]

    print(f"Total posts: {len(ids)}")
    print(f"Unique posts: {len(set(ids))}")

    print("FINAL SELECTED:", len(posts))
    print("TOP REMAINING:", len(top_posts))
    print("OTHER REMAINING:", len(other_posts))
    print("RANDOM REMAINING:", len(random_posts))

    all_remaining = list(top_posts) + list(other_posts) + list(random_posts)

    print(
        "UNSELECTED REMAINING:",
        sum(1 for p in all_remaining if p.id not in selected_post_ids)
    )



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
