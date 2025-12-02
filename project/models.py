# File: models.py
# Author: Dawson Maska (dawsonwm@bu.edu), 11/20/2025
# Description: models file for snake application.  
# Creates the classes that define the data models for the application.

from django.db import models
from django.urls import reverse
from colorfield.fields import ColorField

class Bot(models.Model):
    """Encapsulate the data of a snake bot"""

    name = models.CharField(max_length=30, blank=True)
    author = models.CharField(max_length=30, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    # Snake color in hex format
    color = ColorField(default="#00FF00")

    # User provided bot weights

    # How much the bot beelines for food - 0 to 2
    greediness = models.FloatField(default=0.5)

    # How much space around the head the bot prefers - 0 to 2
    caution = models.FloatField(default=0.5)

    # What direction preference the bot has - -1 to 1
    direction_bias = models.FloatField(default=0.0)

    # How much the bot prefers to circle - 0 to 2
    circliness = models.FloatField(default=0.5)

    # How much the bot ignores the optimal move based on the rest of its personality to be quirky - 0 to 1
    chaos = models.FloatField(default=0.1)

    def __str__(self):
        return f"Bot {self.name} by {self.author}:\n\
        Greediness: {self.greediness}\n\
        Caution: {self.caution} \n\
        Direction Bias: {self.direction_bias} \n\
        Circliness: {self.circliness} \n\
        Chaos: {self.chaos}"
    
    def get_absolute_url(self):
        return reverse('bots', args=[str(self.id)])

class Board(models.Model):
    """Encapsulate the data of a snake board"""

    width = models.IntegerField(default=20)
    height = models.IntegerField(default=20)
    #Creator of the board
    author = models.CharField(max_length=30, blank=True)
    #How many food pieces are on the board at once
    food_count = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now=True)
    
    #JSON representation of the saved board.
    board_json = models.JSONField(blank=False)

    def __str__(self):
        return f"Board {self.id} by {self.author}: {self.width}x{self.height} with {self.food_count} food items."
    
    def get_absolute_url(self):
        return reverse('boards', args=[str(self.id)])

class Match(models.Model):
    """Encapsulate the data of a Match between two Bots on a Board"""
    bot1 = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='bot1_matches')
    bot2 = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='bot2_matches')
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    winner = models.IntegerField(blank=True, null=True)  # 1 if bot1 wins, 2 if bot2 wins, 0 for draw

    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(auto_now=True)

    # Game statistics
    total_turns = models.PositiveIntegerField(default=0)
    apples_a = models.PositiveIntegerField(default=0)
    apples_b = models.PositiveIntegerField(default=0)

    # How many turns each bot survived (great for plotly graphs to compare bots)  
    # A bot could theoretically win scorewise but have a lower survival time if it focused on eating apples quickly
    a_survival_time = models.PositiveIntegerField(default=0)  
    b_survival_time = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return f"Match {self.id} between {self.bot1.name} and {self.bot2.name} won by {'Bot 1' if self.winner == 1 else 'Bot 2' if self.winner == 2 else 'NIETHER'} after {self.total_turns} turns.  Score: {self.apples_a}-{self.apples_b}"
    
    def get_moves(self):
        """Get all move events for this match ordered by move number"""
        return self.move_events.order_by('move_number')

class MoveEvent(models.Model):
    """Encapsulate a single move event in a Match"""

    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='move_events')
    move_number = models.IntegerField()

    #Store the bots absolute move direction
    bot1_move = models.CharField(max_length=5)  # 'UP', 'DOWN', 'LEFT', 'RIGHT'
    bot2_move = models.CharField(max_length=5)

    #Store the head position of the bots (body positions can be derived from this and the board state)
    bot1_head_x = models.IntegerField()
    bot1_head_y = models.IntegerField()
    bot2_head_x = models.IntegerField()
    bot2_head_y = models.IntegerField()

    # Location of the apple positions 
    apple_positions = models.JSONField(blank=False)

    # Did snakes just eat an apple (Would have caused apple positions to change, so need to track it)
    bot1_ate = models.BooleanField(default=False)
    bot2_ate = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Move {self.move_number} in Match {self.match.id}: Bot1 move {self.bot1_move} to ({self.bot1_head_x},{self.bot1_head_y}), Bot2 move {self.bot2_move} to ({self.bot2_head_x},{self.bot2_head_y}). Apples at {self.apple_positions}."