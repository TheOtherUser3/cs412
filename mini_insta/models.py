# File: models.py
# Author: Dawson Maska (dawsonwm@bu.edu), 9/23/2025
# Description: models file for mini_insta application.  
# Creates the classes that define the data models for the application.

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    """Encapsulate the data of a mini_insta Profile of a user"""
    # Define the data attribute of a Profile
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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

    def get_absolute_url(self):
        """Return the url to access a particular profile instance."""
        return reverse('show_profile', kwargs={'pk':self.pk})
    
    def get_followers(self):
        """Return a list of the Profiles of all followers of this Profile instance."""
        follows = Follow.objects.filter(profile=self)
        followers = []
        for follow in follows:
            followers.append(follow.follower_profile)
        return followers
    
    def get_num_followers(self):
        """Return the number of followers of this Profile instance."""
        return Follow.objects.filter(profile=self).count()
    
    def get_following(self):
        """Return a list of the Profiles that this Profile instance is following."""
        follows = Follow.objects.filter(follower_profile=self)
        following = []
        for follow in follows:
            following.append(follow.profile)
        return following
    
    def get_num_following(self):
        """Return the number of Profiles that this Profile instance is following."""
        return Follow.objects.filter(follower_profile=self).count()
    
    def get_post_feed(self):
        """Return a list of Posts from Profiles that this Profile instance is following, ordered by timestamp"""
        following = self.get_following()
        posts = Post.objects.filter(profile__in=following)
        return posts.order_by('-timestamp')
    
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
    
    def get_all_comments(self):
        """Return all comments associated with this Post instance."""
        comments = Comment.objects.filter(post=self)
        return comments.order_by('timestamp')
    
    def get_likes(self):
        """Return all likes associated with this Post instance."""
        likes = Like.objects.filter(post=self)
        return likes.order_by('-timestamp')
    
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
        
class Follow(models.Model):
    """Encapsulate the data of a mini_insta Follow relationship between two Profiles"""
    # Define the data attributes of a Follow relationship
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower_profile')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human-readable representation of the model instance."""
        return f"{self.follower_profile.username} follows {self.profile.username}"
    
class Comment(models.Model):
    """Encapsulate the data of a mini_insta Comment on a Post"""
    # Define the data attributes of a Comment
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human-readable representation of the model instance."""
        return f"Comment by {self.profile.username} on Profile {self.profile.username} and Post ID: {self.post.id}: {self.text[:30]}..."
    
class Like(models.Model):
    """Encapsulate the data of a mini_insta Like on a Post"""
    # Define the data attributes of a Like
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human-readable representation of the model instance."""
        return f"Like by {self.profile.username} on Post ID: {self.post.id}"