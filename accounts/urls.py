from django.urls import path
from accounts.views import *
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name="register"),
    path('login/', login_auth, name="login"),
    path('user/<int:id>', profile, name="profile"),
    path('log-out', LogoutView.as_view(), name='log-out'),
    path('edit-profile/', edit_profile, name="edit-profile"),
]
