# File: forms.py
# Author: Dawson Maska (dawsonwm@bu.edu), 11/21/2025
# Description: forms file that defines forms for snake application.

from django import forms
from .models import *
 

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
    (100, "100x60 (Jumbo Arena)"),
    (80, "80x48 (Huge Arena)"),
    (60, "60x36 (Extra Large Arena)"),
    (50, "50x30 (Large Arena)"),
    (40, "40x24 (Medium)"),
    (25, "25x15 (Standard)"),
    (20, "20x12 (Compact)"),
    (10, "10x6 (Tiny Duel Arena)"),
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

    introversion = forms.FloatField(
        label="Introversion",
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
        fields = ['name', 'color', 'greediness', 'caution', 'direction_bias', 'circliness', 'introversion', 'chaos']
        # Color picker widget
        widgets = {
            "color": forms.TextInput(attrs={"type": "color"}),
        }

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
        fields = ['name', 'board_type', 'grid_width', 'num_apples', 'wraparound']

class BoardUpdateForm(forms.ModelForm):
    """Define a form to update an existing Board"""

    num_apples = forms.ChoiceField(
        label="Number of Apples",
        choices=APPLE_OPTIONS
    )

    class Meta:
        model = Board
        fields = ['name', 'num_apples']


#Use a forms.form for what we are doing here since we DO NOT immediately make the match
class StartMatchForm(forms.Form):
    """Define a form to start a new Match"""

    bot1 = forms.ModelChoiceField(
        queryset=Bot.objects.all(),
        label="Bot 1"
    )

    bot2 = forms.ModelChoiceField(
        queryset=Bot.objects.all(),
        label="Bot 2"
    )

    board = forms.ModelChoiceField(
        queryset=Board.objects.all(),
        label="Board"
    )

class SimulationForm(forms.Form):
    """Define a form to simulate runs number of matches"""
    bot1 = forms.ModelChoiceField(queryset=Bot.objects.all(), label = "Bot 1")

    bot2 = forms.ModelChoiceField(queryset=Bot.objects.all(), label = "Bot 2")

    board = forms.ModelChoiceField(queryset=Board.objects.all(), label = "Board")

    runs = forms.IntegerField(min_value=5, max_value=50, initial=20, label = "Number of Simulations")