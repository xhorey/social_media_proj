from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.http import HttpResponse
from .models import Profile
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
    return render(request, 'Main_Web_Page.html')

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
    return render(request, 'settings.html')

@login_required(login_url='signin')
def posting(request):
    return render(request, 'post.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')