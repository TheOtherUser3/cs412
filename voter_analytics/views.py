# File: views.py
# Author: Dawson Maska (dawsonwm@bu.edu), 10/28/2025
# Description: views file that calls on the html templates when called on 
# by urls.py and does any additional logic required to display the desired page

from django.shortcuts import render

# Create your views here.

def test():
    return render("This is a test view for voter analytics.")