# File: urls.py
# Author: Dawson Maska (dawsonwm@bu.edu), 9/16/2025
# Description: urls file for restaurant application.  
# Sends HTTPS request to matching views.py function
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.main, name="main_page"),
    path('order/', views.order, name="order_page"),
    path('submit', views.submit, name="submit"),
] 