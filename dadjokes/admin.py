# File: admin.py
# Author: Dawson Maska (dawsonwm@bu.edu), 11/12/2025
# Description: Admin configuration for dadjokes application.
# Registers models with Django admin interface.


from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(Joke)
admin.site.register(Picture)