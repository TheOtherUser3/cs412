# File: urls.py
# Author: Dawson Maska (dawsonwm@bu.edu), 11/20/2025
# Description: urls file for snake application.  
# Sends HTTPS request to matching views.py function

from .views import *
from django.urls import path

urlpatterns = [
    path('', HomePageTemplateView.as_view(), name="home_page"),
    path("test/<str:page>/", test_page, name="test_page"),
]