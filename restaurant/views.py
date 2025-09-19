# File: views.py
# Author: Dawson Maska (dawsonwm@bu.edu), 9/16/2025
# Description: views file that calls on the html templates when called on 
# by urls.py and does any additional logic required to display the desired page

from django.shortcuts import render
import random
import time
# Create your views here.

#Daily Special Options
daily_specials = [
    "The Bean Feast Platter",
    "Bean Buffet",
    "Chef's Choice Bean Surprise",
    "Just Regular Beans",
    "Beans on Toast",
    "Bucket o' Beans",
    "One Big Bean",
    "Pumpkin Spice Beans",
    "Cheeseburger"
]

def main(request):
    """Respond to the URL '' to display the home page, delegate work to a template and
    returns the rendered web page as HTTP response
    """
    # Path to the html template
    template_name = 'restaurant/main.html'

    return render(request, template_name)

def order(request):
    '''Show the order form to the user'''
    #Import context variable for daily special
    context = {
        'daily_special': random.choice(daily_specials)
    }
    template_name = "restaurant/order.html"
    return render(request, template_name, context)

def submit(request):
    '''process the submitted form, generate result'''
    template_name = "restaurant/confirmation.html"
    print(request)
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        daily_special = request.POST.get('daily_special', None)
        #Name of the daily special
        daily_special_type = request.POST.get('daily_special_type', None)

        ultimate_bean_experience = request.POST.get('ultimate_bean_experience', 0)
        side_of_beans = request.POST.get('side_of_beans', None)

        mystery_bean_stew = request.POST.get('mystery_bean_stew', 0)

        bean_salad = request.POST.get('bean_salad', 0)
        bean_dressing = request.POST.get('bean_dressing', None)

        bean_on_a_plate = request.POST.get('bean_on_a_plate', 0)
        bean_dust = request.POST.get('bean_dust', None)

        extra_delay = None

        #Get expected time for order (comically long wait)

        #10 to 25 minutes per ultimate bean experience ordered
        quantity = int(ultimate_bean_experience)*random.randint(10,25)
        #2 to 5 minutes per side of beans ordered
        if side_of_beans:
            quantity = quantity + random.randint(2,5)
        #5 to 15 minutes per mystery bean stew ordered
        quantity = quantity + int(mystery_bean_stew)*random.randint(5,15) 
        #3 to 13 minutes per bean salad ordered
        quantity = quantity + int(bean_salad)*random.randint(3,13)
        #Up to 5 extra minutes for bean dressing
        if bean_dressing:
            quantity = quantity + random.randint(0,5)
        #1 to 3 minutes per bean on a plate ordered
        quantity = quantity + int(bean_on_a_plate)*random.randint(1,3)
        #14 to 34 minutes to grind bean dust from scratch
        if bean_dust:
            quantity = quantity + random.randint(14,34)
        #10 to 80 added for daily special
        if daily_special:
            quantity = quantity + random.randint(10,80)
        #minimum wait time of 10 minutes
        quantity = quantity if quantity > 0 else 10 
        
        #10 percent chance of unexpected delays adding 2 to 24 hours
        if random.random() < 0.1:
            quantity = quantity + random.randint(120, 1440)
            extra_delay = 1

        ready_time = time.strftime("%D %I:%M %p", time.localtime(time.time() + quantity*60))

        total_cost = int(ultimate_bean_experience)*31 + (5 if side_of_beans else 0) + \
            int(mystery_bean_stew)*22 + int(bean_salad)*12 + (3 if bean_dressing else 0) + \
            int(bean_on_a_plate)*15 + (4 if bean_dust else 0) + (18 if daily_special else 0)
        
         # Create the context dictionary to pass to the template
        context = {
            'name': name, 
            'email': email,
            'daily_special': daily_special,
            'daily_special_type': daily_special_type,
            'ultimate_bean_experience': ultimate_bean_experience,
            'ultimate_bean_experience_cost': int(ultimate_bean_experience)*31,
            'side_of_beans': side_of_beans,
            'mystery_bean_stew': mystery_bean_stew,
            'mystery_bean_stew_cost': int(mystery_bean_stew)*22,
            'bean_salad': bean_salad,
            'bean_salad_cost': int(bean_salad)*12,
            'bean_dressing': bean_dressing,
            'bean_on_a_plate': bean_on_a_plate,
            'bean_on_a_plate_cost': int(bean_on_a_plate)*15,
            'bean_dust': bean_dust,
            'ready_time': ready_time,
            "quantity": quantity,
            "extra_delay": extra_delay,
            "total_cost": total_cost
        }
        return render(request, template_name, context)

    template_name = "restaurant/order.html"
    return render(request, template_name)