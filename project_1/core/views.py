from django.shortcuts import render
from django.http import HttpResponse


def signin(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'Main_Web_Page.html')

def signup(request):
    return render(request, 'Signup.html')
