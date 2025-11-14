# File: urls.py
# Author: Dawson Maska (dawsonwm@bu.edu), 11/11/2025
# Description: urls file for dadjokes application.  
# Sends HTTPS request to matching views.py function

from .views import *
from django.urls import path

urlpatterns = [
    path('', JokePictureTemplateView.as_view(), name="home_page"),
    path('random/', JokePictureTemplateView.as_view(), name="random"),
    path('jokes/', JokeListView.as_view(), name='jokes'),
    path('joke/<int:pk>/', JokeDetailView.as_view(), name='joke'),
    path('pictures/', PictureListView.as_view(), name='pictures'),
    path('picture/<int:pk>/', PictureDetailView.as_view(), name='picture'),
    ### API paths
    path('api/', JokeRandomAPIView.as_view()),
    path('api/random/', JokeRandomAPIView.as_view()),
    path('api/jokes/', JokeListAPIView.as_view()),
    path('api/joke/<int:pk>/', JokeDetailAPIView.as_view()),
    path('api/pictures/', PictureListAPIView.as_view()),
    path('api/picture/<int:pk>/', PictureDetailAPIView.as_view()),
    path('api/random_picture', PictureRandomAPIView.as_view()),

]