# File: views.py
# Author: Dawson Maska (dawsonwm@bu.edu), 9/23/2025
# Description: views file that calls on the html templates when called on 
# by urls.py and does any additional logic required to display the desired page

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile
import random

# Create your views here.

class ProfileListView(ListView):
    """Define a view class to show all mini_insta Profiles"""
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'
