# File: views.py
# Author: Dawson Maska (dawsonwm@bu.edu), 11/11/2025
# Description: views file that calls on the html templates when called on 
# by urls.py and does any additional logic required to display the desired page

from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Joke, Picture
from django.urls import reverse
from random import choice

class JokePictureTemplateView(TemplateView):
    """Define a view class to display a random joke and picture"""
    template_name = 'dadjokes/random.html'

    def get_context_data(self, **kwargs):
        """Override this method to add in a random joke and picture to the context"""
        context = super().get_context_data(**kwargs)

        # Idea taken from lovely Stack Overflow user km6 for maximum efficiency
        # only need to load all pks, rather than all objects

        pks = Joke.objects.values_list('pk', flat=True)
        random_pk = choice(pks)
        joke = Joke.objects.get(pk=random_pk)

        pks = Picture.objects.values_list('pk', flat=True)
        random_pk = choice(pks)
        picture = Picture.objects.get(pk=random_pk)

        context['joke'] = joke
        context['picture'] = picture
        
        return context

class JokeListView(ListView):
    """Define a view class to display all jokes"""
    model = Joke
    template_name = 'dadjokes/jokes.html'
    context_object_name = 'jokes'

class JokeDetailView(DetailView):
    """Define a view class to display a specific joke"""
    model = Joke
    template_name = 'dadjokes/joke.html'
    context_object_name = 'joke'

class PictureListView(ListView):
    """Define a view class to display all pictures"""
    model = Picture
    template_name = 'dadjokes/pictures.html'
    context_object_name = 'pictures'

class PictureDetailView(DetailView):
    """Define a view class to display a specific picture"""
    model = Picture
    template_name = 'dadjokes/picture.html'
    context_object_name = 'picture'

################################################################################
# enable the REST API for this application
from rest_framework import generics
from .serializers import *

class JokeListAPIView(generics.ListCreateAPIView):
    """This view will expose the API for Jokes with List and Create"""
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class JokeRandomAPIView(generics.RetrieveAPIView):
    """Exposes the API for a single random joke"""
    # Use clever code from km6 for maximum efficiency
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

    def get_object(self):
        """Override to get a random joke"""
        pks = Joke.objects.values_list('pk', flat=True)
        random_pk = choice(pks)
        return Joke.objects.get(pk=random_pk)

class JokeDetailAPIView(generics.RetrieveAPIView):
    """Exposes the API to return a single Joke by primary key"""
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class PictureListAPIView(generics.ListAPIView):
    """Exposes the API to return all Pictures"""
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class PictureDetailAPIView(generics.RetrieveAPIView):
    """Exposes the API to return all Pictures"""
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

    def get_object(self):
        """Override to get a random picture"""
        pks = Picture.objects.values_list('pk', flat=True)
        random_pk = choice(pks)
        return Picture.objects.get(pk=random_pk)

class PictureRandomAPIView(generics.RetrieveAPIView):
    """Exposes the API for a single random Picture"""
    # Use clever code from km6 for maximum efficiency
    queryset = Picture.objects.all()
    serializer_class = JokeSerializer

    def get_object(self):
        """Override to get a random joke"""
        pks = Picture.objects.values_list('pk', flat=True)
        random_pk = choice(pks)
        return Picture.objects.get(pk=random_pk)