# File: views.py
# Author: Dawson Maska (dawsonwm@bu.edu), 11/20/2025
# Description: views file that calls on the html templates when called on 
# by urls.py and does any additional logic required to display the desired page

from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import *
from django.urls import reverse
from random import choice
from django.http import HttpResponse

class HomePageTemplateView(TemplateView):
    """Define a view class to display the home snake navigation page"""
    template_name = 'project/home_page.html'

def test_page(request, page):
    return HttpResponse(f"<h1>{page} page placeholder</h1>")

################################################################################
# enable the REST API for this application
from rest_framework import generics
from .serializers import *


