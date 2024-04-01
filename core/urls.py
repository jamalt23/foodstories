from django.urls import path
from core.views import *

app_name = 'core'

urlpatterns = [
    path('', home, name="home"),
    path('post/<int:id>', detail, name="detail")
]                                                  