# File: views.py
# Author: Dawson Maska (dawsonwm@bu.edu), 9/23/2025
# Description: views file that calls on the html templates when called on 
# by urls.py and does any additional logic required to display the desired page

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm
from django.urls import reverse

# Create your views here.

class ProfileListView(ListView):
    """Define a view class to show all mini_insta Profiles"""
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    """Define a view class to show a specific mini_insta Profile"""
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

class PostDetailView(DetailView):
    """Define a view class to show a specific mini_insta Post"""
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

class CreatePostView(CreateView):
    """Define a view class to create a new Post for a specific Profile"""
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_context_data(self, **kwargs):
        """Add the profile to the context data for the template"""
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        """Set the profile of the new Post to the Profile in the URL
        and create and set the Photo to the Post"""
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile
        post = form.save()
        post.save()
        # if not self.request.POST.get('image_url'):
        #     return super().form_valid(form)
        # photo = Photo()
        # photo.image_url = self.request.POST.get('image_url')
        # photo.post = post
        # photo.save()
        #Make all new photos, set their attributes, and save them
        files = self.request.FILES.getlist('image_file')
        for file in files:
            photo = Photo()
            photo.image_file = file
            photo.post = post
            photo.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        """After creating a post, return to the profile page"""
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        pk = profile.pk
        return reverse('show_profile', kwargs={'pk':pk})

class UpdateProfileView(UpdateView):
    """Define a view class to update a specific profile"""

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

class DeletePostView(DeleteView):
    """Define a View class to delete a specific post instance"""

    model = Post
    template_name = 'mini_insta/delete_post_form.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        """override the method to provide the 
        profile instance as a context variable"""
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        profile = post.profile
        context = super().get_context_data(**kwargs)
        context['profile'] = profile
        return context
    
    def get_success_url(self):
        """Send user to the profile the deleted post corresponded to"""
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        profile = post.profile
        return reverse('show_profile', kwargs={'pk':profile.pk})
    
class UpdatePostView(UpdateView):
    """Define a view class to update a post instance"""

    model = Post
    # CreatePostForm already handles the caption, no need to
    # make a new form to do the exact same thing
    form_class = CreatePostForm
    template_name = 'mini_insta/update_post_form.html'

    def get_context_data(self, **kwargs):
        """override the method to provide the 
        profile instance as a context variable"""
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        profile = post.profile
        context = super().get_context_data(**kwargs)
        context['profile'] = profile
        return context
    
    def get_success_url(self):
        """Send user to the updated post"""
        pk = self.kwargs['pk']
        return reverse('show_post', kwargs={'pk':pk})
