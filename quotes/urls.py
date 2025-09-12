# File: urls.py
# Author: Dawson Maska (dawsonwm@bu.edu), 9/9/2025
# Description: urls file for quotes application.  
# Sends HTTPS request to matching views.py function

from django.urls import path
from django.conf import settings
from . import views


urlpatterns = [
    # Main page: displays picture of Joe Biden and a quote he said  
    # or wrote.  Selected at random from a list of images/quotes.
    path('',views.home, name="home_page"),
    # Similar to main, generates one quote and one image at random.
    path('quote/', views.quote, name="quote_page"),
    # An ancillary page that shows all quotes and images
    path('show_all/', views.show_all, name="show_all_page"),
    # An about page with short biographical information about Joe Biden,
    # as well as a note about the creator (me).
    path('about/', views.about, name="about_page"),
]