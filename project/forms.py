# File: forms.py
# Author: Dawson Maska (dawsonwm@bu.edu), 11/21/2025
# Description: forms file that defines forms for snake application.

from django import forms
from .models import *

from colorfield.widgets import ColorWidget

class CreateBotForm(forms.ModelForm):
    """Define a form to create a new Bot"""

    name = forms.CharField(max_length=30, label='Bot Name')
    author = forms.CharField(max_length=30, label='Author Name')

    # Get color using a color picker
    color = forms.CharField(widget=ColorWidget, label='Bot Color')

    # Define sliders for personality weights

    greediness = forms.FloatField(
        label="Greediness",
        initial = 0.5,
        min_value=0,
        max_value=2,
        widget=forms.NumberInput(attrs={
            'type': 'range',   # make a slider
            'step': '0.05',     # float increments
            'min': '0',
            'max': '2'
        })
    )

    caution = forms.FloatField(
        label="Caution",
        initial = 0.5,
        min_value=0,
        max_value=2,
        widget=forms.NumberInput(attrs={
            'type': 'range',   # make a slider
            'step': '0.05',     # float increments
            'min': '0',
            'max': '2'
        })
    )

    direction_bias = forms.FloatField(
        label="Turning Bias, Left to Right",
        initial = 0.0,
        min_value=-1,
        max_value=1,
        widget=forms.NumberInput(attrs={
            'type': 'range',   # make a slider
            'step': '0.05',     # float increments
            'min': '-1',
            'max': '1'
        })
    )

    circliness = forms.FloatField(
        label="Circliness",
        initial = 0.5,
        min_value=0,
        max_value=2,
        widget=forms.NumberInput(attrs={
            'type': 'range',   # make a slider
            'step': '0.05',     # float increments
            'min': '0',
            'max': '2'
        })
    )

    chaos = forms.FloatField(
        label="Chaos Factor",
        initial = 0.1,
        min_value=0,
        max_value=1,
        widget=forms.NumberInput(attrs={
            'type': 'range',   # make a slider
            'step': '0.025',     # float increments
            'min': '0',
            'max': '1'
        })
    )

    class Meta:
        model = Bot
        fields = ['name', 'author', 'color', 'greediness', 'caution', 'direction_bias', 'circliness', 'chaos']
