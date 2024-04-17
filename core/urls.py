from django.urls import path
from core.views import *

app_name = 'core'

urlpatterns = [
    path('', home, name="home"),
    path('post/<int:id>', detail, name="detail"),
    path('about/', about, name="about"),
    path('stories', stories, name="stories"),
    path('stories/', stories, name="stories"),
    path('stories/?category=<str:category>', stories, name="stories"),
    path('stories/?tag=<str:tag>', stories, name="stories"),
    path('stories/?tag=<str:tag>&category=<str:category>', stories, name="stories"),
    path('stories/?category=<str:category>&tag=<str:tag>', stories, name="stories"),
    path('recipes/', recipes, name="recipes"),
    path('contact/', contact, name="contact"),
    path('create-post/', create_post, name="create-post"),
]
