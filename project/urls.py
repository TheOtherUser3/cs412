# File: urls.py
# Author: Dawson Maska (dawsonwm@bu.edu), 11/20/2025
# Description: urls file for snake application.  
# Sends HTTPS request to matching views.py function

from .views import *
from django.urls import path

urlpatterns = [
    path('', HomePageTemplateView.as_view(), name="home_page"),

    #Bots
    path('bots/', BotListView.as_view(), name="bots"),
    path('bots/create/', CreateBotView.as_view(), name="create_bot"),
    path('bots/<int:pk>/delete/', DeleteBotView.as_view(), name="delete_bot"),
    path('bots/<int:pk>/update/', UpdateBotView.as_view(), name="update_bot"),
    path("bots/<int:pk>/", BotDetailView.as_view(), name="bot"),

    #Boards
    path('boards/', BoardListView.as_view(), name="boards"),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name="board"),
    path('boards/create/', CreateBoardView.as_view(), name="create_board"),
    path('boards/<int:pk>/delete/', DeleteBoardView.as_view(), name="delete_board"),
    path('boards/<int:pk>/update/', UpdateBoardView.as_view(), name="update_board"),

    #Matches
    path('matches/', MatchListView.as_view(), name="matches"),    
    path('matches/all/', MatchListView.as_view(), name="matches"),
    path('matches/all/<int:pk>/', MatchDetailView.as_view(), name="match"),
    path('matches/create/', MatchCreateView.as_view(), name="new_match"),
    path('matches/<int:pk>/replay/', MatchReplayView.as_view(), name="match_replay"),
    path('matches/<int:pk>/delete/', MatchDeleteView.as_view(), name="delete_match"),

    #Leaderboards
    path('leaderboards/', LeaderboardHubView.as_view(), name="leaderboards"),
    path('leaderboards/simulate/', SimulationView.as_view(), name="simulate"),
    path('leaderboards/global_leaderboard/', GlobalLeaderboardView.as_view(), name="global_leaderboard"),
    path('leaderboards/board_leaderboard/', BoardLeaderboardHubView.as_view(), name="board_leaderboard_hub"),
    path('leaderboards/board_leaderboard/<int:pk>/', BoardLeaderboardView.as_view(), name="board_leaderboard"),


    # Allows the JS to access MoveEvents via API by passing in match pk (clarified variable name since it's match not move event and that is a little confusing)
    path('api/move_events/<int:match_pk>/', MoveEventListAPIView.as_view(), name="move_events_api"),
]