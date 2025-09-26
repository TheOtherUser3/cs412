# File: urls.py
# Author: Dawson Maska (dawsonwm@bu.edu), 9/23/2025
# Description: urls file for mini_insta application.  
# Sends HTTPS request to matching views.py function

from .views import ProfileListView, ProfileDetailView
from django.urls import path

urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name="show_profile"),
]