# File: models.py
# Author: Dawson Maska (dawsonwm@bu.edu), 9/23/2025
# Description: models file for mini_insta application.  
# Creates the classes that define the data models for the application.

from django.db import models

# Create your models here.

class Profile(models.Model):
    """Encapsulate the data of a mini_insta Profile of a user"""
    # Define the data attribute of a Profile
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human-readable representation of the model instance."""
        return f"Username: {self.username} Display Name: {self.display_name}"