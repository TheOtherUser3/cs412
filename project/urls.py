# File: urls.py
# Author: Dawson Maska (dawsonwm@bu.edu), 11/20/2025
# Description: urls file for snake application.  
# Sends HTTPS request to matching views.py function

from .views import *
from django.urls import path

urlpatterns = [
    path('', HomePageTemplateView.as_view(), name="home_page"),
    path('bots/', BotListView.as_view(), name="bots"),
    path('bots/create/', CreateBotView.as_view(), name="create_bot"),
    path('boards/', BoardListView.as_view(), name="boards"),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name="board"),
    path('boards/create/', CreateBoardView.as_view(), name="create_board"),
    path('boards/<int:pk>/delete/', DeleteBoardView.as_view(), name="delete_board"),
    path('boards/<int:pk>/update/', UpdateBoardView.as_view(), name="update_board"),
    path('matches/', MatchListView.as_view(), name="matches")
    # path('matches/all/', MatchListView.as_view(), name="matches"),
    # path('matches/all/<int:pk>/', MatchDetailView.as_view(), name="match"),
    # path('matches/create/', CreateMatchView.as_view(), name="create_match"),
]