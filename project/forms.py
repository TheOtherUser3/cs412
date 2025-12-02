# File: forms.py
# Author: Dawson Maska (dawsonwm@bu.edu), 11/21/2025
# Description: forms file that defines forms for snake application.

from django import forms
from .models import *

from colorfield.fields import ColorField
from colorfield.widgets import ColorWidget  

# Define constants for board generation
BOARD_TYPES = [
    ("open", "Open Field (No Obstacles)"),
    ("outer_wall", "Outer Walls"),
    ("inner_maze", "Inner Maze"),
    ("scattered_blocks", "Random Scattered Blocks"),
    ("corridors", "Corridor Maze"),
    ("two_box_arenas", "Twin Box Arenas"),
]

BOARD_SIZES = [
    (100, "100×60 (Jumbo Arena)"),
    (80, "80×48 (Huge Arena)"),
    (60, "60×36 (Extra Large Arena)"),
    (50, "50×30 (Large Arena)"),
    (40, "40×24 (Medium)"),
    (25, "25×15 (Standard)"),
    (20, "20×12 (Compact)"),
    (10, "10×6 (Tiny Duel Arena)"),
]

APPLE_OPTIONS = [
    (1, "1 Apple"),
    (2, "2 Apples"),
    (3, "3 Apples"),
    (5, "5 Apples"),
    (8, "8 Apples"),
    (10, "10 Apples"),
]

class CreateBotForm(forms.ModelForm):
    """Define a form to create a new Bot"""

    name = forms.CharField(max_length=30, label='Bot Name')
    author = forms.CharField(max_length=30, label='Author Name')

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

class BoardGeneratorForm(forms.ModelForm):
    """Define a form to generate a new Board"""
    board_type = forms.ChoiceField(
        label="Board Layout",
        choices=BOARD_TYPES
    )

    grid_width = forms.ChoiceField(
        label="Grid Width",
        choices=BOARD_SIZES
    )

    num_apples = forms.ChoiceField(
        label="Number of Apples",
        choices=APPLE_OPTIONS
    )

    wraparound = forms.BooleanField(
        label="Enable Wraparound Edges",
        required=False)

    class Meta:
        model = Board
        fields = ['board_type', 'grid_width', 'num_apples', 'wraparound', 'author']