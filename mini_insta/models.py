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
    
    def get_all_posts(self):
        """Return all posts associated with this Profile instance."""
        # Get all Posts
        posts = Post.objects.filter(profile=self)
        # Order posts by timestamp, most recent first
        posts = posts.order_by('-timestamp')
        return posts
    
class Post(models.Model):
    """Encapsulate the data of a mini_insta Post attached to a Profile"""
    # Define the data attributes of a Post
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human-readable representation of the model instance."""
        return f"Post by {self.profile.username} with caption: {self.caption[:30]}..."
    
    def get_all_photos(self):
        """Return all photos associated with this Post instance."""
        return Photo.objects.filter(post=self)
    
class Photo(models.Model):
    """Encapsulate the data of a mini_insta Photo attached to a Post"""
    # Define the data attributes of a Photo
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human-readable representation of the model instance."""
        if self.image_url:
            return f"Photo for Post ID: {self.post.id} with URL: {self.image_url}"
        else:
            return f"Photo for Post ID: {self.post.id} with URL: {self.image_file.url}"
    
    def get_image_url(self):
        """Get the url to access an image, either from image_url if it exists or from image_file.url"""
        if self.image_url:
            return self.image_url
        else:
            return self.image_file.url