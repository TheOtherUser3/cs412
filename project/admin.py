# File: admin.py
# Author: Dawson Maska (dawsonwm@bu.edu), 11/21/2025
# Description: Admin configuration for snake arena application.
# Registers models with Django admin interface.

from django.contrib import admin
from .models import Bot, Board, Match, MoveEvent
# Register your models here.

admin.site.register(Bot)
admin.site.register(Board) 
admin.site.register(Match)
admin.site.register(MoveEvent)

