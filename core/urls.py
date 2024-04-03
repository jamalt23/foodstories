from django.urls import path
from core.views import *

app_name = 'core'

urlpatterns = [
    path('', home, name="home"),
    path('post/<int:id>', detail, name="detail"),
    path('about', about, name="about"),
    path('stories', stories, name="stories"),
    path('stories/', stories, name="stories"),
    path('stories/<str:category>', stories, name="stories"),
    path('recipes', recipes, name="recipes"),
    path('contact', contact, name="contact"),
]
