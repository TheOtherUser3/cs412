# File: urls.py
# Author: Dawson Maska (dawsonwm@bu.edu), 9/23/2025
# Description: urls file for mini_insta application.  
# Sends HTTPS request to matching views.py function

from .views import *
from django.urls import path

urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name="show_profile"),
    path('profile/post/<int:pk>/', PostDetailView.as_view(), name="show_post"),
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name='create_post'),
    path('profile/<int:pk>/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('profile/post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name='show_following'),
    path('profile/<int:pk>/feed', PostFeedListView.as_view(), name = "show_feed"),
]