# File: urls.py
# Author: Dawson Maska (dawsonwm@bu.edu), 11/20/2025
# Description: urls file for snake application.  
# Sends HTTPS request to matching views.py function

from .views import *
from django.urls import path

urlpatterns = [
    path('', HomePageTemplateView.as_view(), name="home_page"),
    path('bots/<int:pk>/', BotListView.as_view(), name="bots"),
    path('bots/create/', CreateBotView.as_view(), name="create_bot"),
    path('boards/', BoardListView.as_view(), name="boards"),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name="board"),
    path('boards/create/', CreateBoardView.as_view(), name="create_board"),
]