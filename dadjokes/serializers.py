# # File: serializers.py
# Author: Dawson Maska (dawsonwm@bu.edu), 11/11/2025
# Description: This file explains how to convert our Django data models
# for transmission over http

from rest_framework import serializers
from .models import *

class JokeSerializer(serializers.ModelSerializer):
    """Specifies which fields are exposed to the API for Jokes"""

    class Meta:
        model = Joke
        fields = ['id','text','name','timestamp']


class PictureSerializer(serializers.ModelSerializer):
    """Specifies which fields are exposed to the API for Pictures"""

    class Meta:
        model = Picture
        fields = ['id','image_url','name','timestamp']


