# File: serializers.py
# Author: Dawson Maska (dawsonwm@bu.edu), 11/20/2025
# Description: This file explains how to convert our Django data models
# for transmission over http - Needed for our Javascript to efficiently access
# our MoveEvents for a Match

from rest_framework import serializers
from .models import *

EXCLUDED_NAMES = ['id', 'match', 'timestamp']

class MoveEventSerializer(serializers.ModelSerializer):
    """Specifies which fields are exposed to the API for MoveEvents"""

    class Meta:
        model = MoveEvent
        field_names = [field.name for field in MoveEvent._meta.get_fields() if field.name not in EXCLUDED_NAMES]
        fields = field_names