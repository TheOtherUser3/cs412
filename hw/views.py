from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
# Create your views here.
import time
import random
def home(request):
    response_text = f'''
    <html>
    <h1> Hello World </h1>
    <body>The current time is {time.ctime()}</body>
    </html>
    '''
    return HttpResponse(response_text)

def home_page(request):
    """Repond to the URL '', delegate work to a template"""
    template_name = 'hw/home.html'
    context = {
        "time": time.ctime(),
        "letter1": random.choice('abcdefghijklmnopqrstuvwxyz'.upper()),
        "letter2": random.choice('abcdefghijklmnopqrstuvwxyz'.upper()),
        "number": random.randint(0,100),
    }
    return render(request, template_name, context)

def about(request):
    """Repond to the URL '', delegate work to a template"""
    template_name = 'hw/about.html'
    context = {
        "time": time.ctime(),
        "letter1": random.choice('abcdefghijklmnopqrstuvwxyz'.upper()),
        "letter2": random.choice('abcdefghijklmnopqrstuvwxyz'.upper()),
        "number": random.randint(0,100),
    }
    return render(request, template_name, context)