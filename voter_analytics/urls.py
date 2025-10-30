# File: urls.py
# Author: Dawson Maska (dawsonwm@bu.edu), 10/28/2025
# Description: urls file for voter_analytics application.  
# Sends HTTPS request to matching views.py function

from .views import *
from django.urls import path

urlpatterns = [
    path('', VotersListView.as_view(), name="voters"),
    path('voter/<int:pk>/', VoterDetailView.as_view(), name="voter"),
    path('graphs/', GraphsListView.as_view(), name='graphs')
]