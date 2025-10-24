# File: urls.py
# Author: Dawson Maska (dawsonwm@bu.edu), 9/23/2025
# Description: urls file for mini_insta application.  
# Sends HTTPS request to matching views.py function

from .views import *
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name="show_profile"),
    path('profile/post/<int:pk>/', PostDetailView.as_view(), name="show_post"),
    path('profile/create_post', CreatePostView.as_view(), name='create_post'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('profile/post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name='show_following'),
    path('profile/feed', PostFeedListView.as_view(), name = "show_feed"),
    path('profile/search', SearchView.as_view(), name="search"),
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name='logout'),
    path('logout/confirmation/', TemplateView.as_view(template_name='mini_insta/logout_confirmation.html'), name='logout_confirmation'),
]