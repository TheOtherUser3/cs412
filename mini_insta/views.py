# File: views.py
# Author: Dawson Maska (dawsonwm@bu.edu), 9/23/2025
# Description: views file that calls on the html templates when called on 
# by urls.py and does any additional logic required to display the desired page

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo, Follow, Like
from .forms import CreatePostForm, UpdateProfileForm, CreateProfileForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect
# Create your views here.

class MiniInstaLoginRequiredMixin(LoginRequiredMixin):
    """Custom LoginRequiredMixin that always redirects to the correct login page."""

    def get_login_url(self):
        """Return the login URL to redirect to for login."""
        return reverse('login')
    
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

class CreatePostView(MiniInstaLoginRequiredMixin, CreateView):
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

class UpdateProfileView(MiniInstaLoginRequiredMixin, UpdateView):
    """Define a view class to update a specific profile"""

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

    def get_object(self):
        """Return the Profile instance to be updated based on user account"""
        # .first to still return a Profile object for the admin profiles
        profile = Profile.objects.filter(user=self.request.user).first()
        return profile

class DeletePostView(MiniInstaLoginRequiredMixin, DeleteView):
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
    
class UpdatePostView(MiniInstaLoginRequiredMixin, UpdateView):
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

class PostFeedListView(MiniInstaLoginRequiredMixin, ListView):
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
    
class SearchView(MiniInstaLoginRequiredMixin, ListView):
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
    
class CreateProfileView(CreateView):
    """Define a view class to create a new Profile and register a new user account"""
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'

    def get_context_data(self, **kwargs):
        """Add the user creation form to the context data for the template"""
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm(prefix="user")
        return context

    def get_success_url(self):
        """Return the URL to direct to after successful registration"""
        return reverse('login')
    
    def form_valid(self, form):
        """Create the User account and associate it with the new Profile"""
        user_form = UserCreationForm(self.request.POST, prefix="user")
        user = user_form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        form.instance.user = user
        return super().form_valid(form)
    
def follow(request, pk):
    """Define a view function to follow a specific profile"""
    profile_to_follow = Profile.objects.get(pk=pk)
    profile = Profile.objects.filter(user=request.user).first()
    follow = Follow()
    follow.profile = profile_to_follow
    follow.follower_profile = profile
    follow.save()
    return redirect('show_profile', pk=pk)

def unfollow(request, pk):
    """Define a view function to unfollow a specific profile"""
    follow = Follow.objects.get(profile__pk=pk, follower_profile=request.user.profile_set.first())
    follow.delete()
    return redirect('show_profile', pk=pk)

def like(request, pk):
    """Define a view function to like a specific post"""
    post_to_like = Post.objects.get(pk=pk)
    profile = Profile.objects.filter(user=request.user).first()
    like = Like()
    like.post = post_to_like
    like.profile = profile
    like.save()
    return redirect('show_post', pk=pk)

def unlike(request, pk):
    """Define a view function to unlike a specific post"""
    like = Like.objects.get(post__pk=pk, profile=request.user.profile_set.first())
    like.delete()
    return redirect('show_post', pk=pk)