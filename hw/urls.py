from django.urls import path
from django.conf import settings
from . import views


urlpatterns = [
    path('',views.home_page, name="home_page"),
    path('about/', views.about, name="about_page"),
]