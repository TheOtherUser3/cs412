# File: models.py
# Author: Dawson Maska (dawsonwm@bu.edu), 11/11/2025
# Description: models file for dadjokes application.  
# Creates the classes that define the data models for the application.

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Joke(models.Model):
    """Encapsulate the data of a dad joke"""

    text = models.TextField(blank=True)
    name = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

class Picture(models.Model):
    """Encapsulate the data of a hilarious image"""

    image_url = models.URLField(blank=True)
    name = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
