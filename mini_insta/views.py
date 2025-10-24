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
        profile = Profile.objects.filter(user=self.request.user).first()
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        """Set the profile of the new Post to the Profile in the URL
        and create and set the Photo to the Post"""
        profile = Profile.objects.filter(user=self.request.user).first()
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
        profile = Profile.objects.filter(user=self.request.user).first()
        pk = profile.pk
        return reverse('show_profile', kwargs={'pk':pk})

class UpdateProfileView(UpdateView):
    """Define a view class to update a specific profile"""

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

    def get_object(self):
        """Return the Profile instance to be updated based on user account"""
        # .first to still return a Profile object for the admin profiles
        profile = Profile.objects.filter(user=self.request.user).first()
        return profile

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

class ShowFollowersDetailView(DetailView):
    """Define a view class to show all followers of a specific Profile"""
    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

class ShowFollowingDetailView(DetailView):
    """Define a view class to show all Profiles a specific Profile is following"""
    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

class PostFeedListView(ListView):
    """Define a view class to show the post feed of a specific Profile"""
    model = Post
    template_name = 'mini_insta/show_feed.html'

    def get_context_data(self, **kwargs):
        """Add the profile to the context data for the template"""
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.filter(user=self.request.user).first()
        context['profile'] = profile
        context['posts'] = profile.get_post_feed()
        return context
    
class SearchView(ListView):
    """Define a view class to search for profiles and posts based on user input"""
    template_name = 'mini_insta/search_results.html'

    def dispatch(self, request, *args, **kwargs):
        """Handle GET and POST requests differently"""
        query = self.request.GET.get('query')
        if query:
            return super().dispatch(request, *args, **kwargs)
        else:
            template_name = 'mini_insta/search.html'
            context = {'profile': Profile.objects.filter(user=self.request.user).first()}
            return render(request, template_name, context)

    def get_queryset(self):
        """Return a list of Posts that match the search query"""
        query = self.request.GET.get('query')
        results = Post.objects.filter(caption__icontains=query)
        return results

    def get_context_data(self, **kwargs):
        """Add the profile and query to the context data for the template"""
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.filter(user=self.request.user).first()
        context['profile'] = profile
        #Get all QuerySets by orring them together and removing duplicates with distinct()
        profiles = (
            Profile.objects.filter(username__icontains=self.request.GET.get('query')) |
            Profile.objects.filter(bio_text__icontains=self.request.GET.get('query')) |
            Profile.objects.filter(display_name__icontains=self.request.GET.get('query'))
        ).distinct()
        posts = self.get_queryset()
        context['profiles'] = profiles.distinct()
        context['posts'] = posts
        context['query'] = self.request.GET.get('query')
        return context
    