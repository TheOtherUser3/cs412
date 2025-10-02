# File: admin.py
# Author: Dawson Maska (dawsonwm@bu.edu), 9/23/2025
# Description: Admin configuration for mini_insta application.
# Registers models with Django admin interface.


from django.contrib import admin

# Register your models here.

from .models import Profile, Post, Photo
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)