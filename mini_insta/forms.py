# File: forms.py
# Author: Dawson Maska (dawsonwm@bu.edu), 10/2/2025
# Description: forms file that defines forms for mini_insta application.

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    """Define a form to create a new Post"""
    class Meta:
        model = Post
        fields = ['caption']
