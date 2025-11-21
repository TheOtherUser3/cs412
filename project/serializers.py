# File: serializers.py
# Author: Dawson Maska (dawsonwm@bu.edu), 11/20/2025
# Description: This file explains how to convert our Django data models
# for transmission over http - Needed for our Javascript to efficiently access
# our MoveEvents for a Match

from rest_framework import serializers
from .models import *