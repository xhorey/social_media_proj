from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('settings', views.settings, name='settings'),
    path('posting', views.posting, name='posting'),
    path('like-post', views.like_post, name='like-post'),
    path('dislike-post', views.dislike_post, name='dislike-post'),
    path('profile/<str:pk>', views.profile, name='profile'),
]