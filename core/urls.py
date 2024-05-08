from django.urls import path
from core.views import *

app_name = 'core'

urlpatterns = [
    path('', home, name="home"),
    path('post/<int:id>', detail, name="detail"),
    path('about/', about, name="about"),
    path('stories/', stories, name="stories"),
    path('contact/', contact, name="contact"),
    path('create-post/', CreatePost.as_view(), name="create-post"),
    path('edit-post/<int:pk>', EditPost.as_view(), name="edit-post"),
    path('search/', stories, name="search"),
]
